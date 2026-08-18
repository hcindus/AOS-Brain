"""
Dark Factory Temporal Activities
Actually do the work. Retryable. Heartbeat-capable.
"""
import os
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from temporalio import activity
import asyncio


class SDKNotInstalledError(Exception):
    """Raised when SDK is not found."""
    pass


class SDKCorruptedError(Exception):
    """Raised when SDK is present but broken."""
    pass


@activity.defn
async def validate_sdk_health(build_type: str) -> dict:
    """
    Validate that the build SDK is installed and functional.
    Raises SDKNotInstalledError or SDKCorruptedError if not.
    """
    activity.logger.info(f"Validating SDK for {build_type}")
    
    if build_type == "apk":
        # Check Android SDK
        sdk_path = os.environ.get("ANDROID_SDK", "/opt/android-sdk")
        if not os.path.exists(sdk_path):
            raise SDKNotInstalledError(f"Android SDK not found at {sdk_path}")
        
        # Quick sanity: can we run sdkmanager?
        sdkmanager = Path(sdk_path) / "cmdline-tools" / "latest" / "bin" / "sdkmanager"
        if not sdkmanager.exists():
            raise SDKCorruptedError("sdkmanager not found")
        
        # Verify build-tools exists
        build_tools = Path(sdk_path) / "build-tools"
        if not build_tools.exists() or not any(build_tools.iterdir()):
            raise SDKCorruptedError("No build-tools installed")
        
        return {"sdk_path": str(sdk_path), "valid": True}
    
    elif build_type == "web":
        # Check Node/npm
        try:
            result = subprocess.run(
                ["node", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                raise SDKNotInstalledError("Node.js not available")
            return {"node_version": result.stdout.strip(), "valid": True}
        except FileNotFoundError:
            raise SDKNotInstalledError("Node.js not installed")
    
    elif build_type == "docker":
        # Check Docker
        try:
            result = subprocess.run(
                ["docker", "version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                raise SDKNotInstalledError("Docker not available")
            return {"docker_available": True, "valid": True}
        except FileNotFoundError:
            raise SDKNotInstalledError("Docker not installed")
    
    return {"valid": True, "message": "No validation needed"}


@activity.defn
async def allocate_build_resources(order_id: str, build_type: str, priority: str) -> dict:
    """
    Allocate workspace and resources for a build.
    Returns resource handles that must be cleaned up.
    """
    activity.logger.info(f"Allocating resources for {order_id}")
    
    # Create workspace
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    workspace = f"/tmp/darkfactory/{order_id}_{timestamp}"
    os.makedirs(workspace, exist_ok=True)
    os.makedirs(f"{workspace}/logs", exist_ok=True)
    os.makedirs(f"{workspace}/output", exist_ok=True)
    
    return {
        "order_id": order_id,
        "workspace": workspace,
        "output_dir": f"{workspace}/output",
        "log_dir": f"{workspace}/logs",
        "priority": priority,
    }


@activity.defn
async def execute_build(order, resources) -> dict:
    """
    Actually execute the build. Heartbeats every 30 seconds.
    `order` arrives as a dict at the activity boundary (Temporal JSON-serializes dataclasses).
    """
    oid = order.get("order_id") if isinstance(order, dict) else order.order_id
    build_type = order.get("build_type") if isinstance(order, dict) else order.build_type
    source = order.get("source_path") if isinstance(order, dict) else order.source_path
    project = order.get("project_name") if isinstance(order, dict) else order.project_name

    activity.logger.info(f"Building {oid}")

    # Send initial heartbeat
    activity.heartbeat("Starting build...")
    
    logs = []
    output_path = None
    file_size = 0
    
    try:
        if build_type == "apk":
            result = await _build_apk(source, resources, logs)
        elif build_type == "web":
            result = await _build_web(source, resources, logs)
        elif build_type == "docker":
            result = await _build_docker(source, project, resources, logs)
        else:
            raise ValueError(f"Unknown build type: {build_type}")
        
        activity.heartbeat("Build complete, verifying...")
        return {
            "success": result["success"],
            "output_path": result.get("output_path"),
            "file_size_bytes": result.get("file_size", 0),
            "logs": logs,
            "error_message": result.get("error"),
        }
        
    except Exception as e:
        activity.logger.error(f"Build failed: {e}")
        return {
            "success": False,
            "output_path": None,
            "file_size_bytes": 0,
            "logs": logs,
            "error_message": str(e),
        }


async def _build_apk(source, resources, logs):
    """Build an Android APK using Bubblewrap or Gradle."""
    import asyncio
    
    output_dir = resources["output_dir"]
    
    # Try Bubblewrap first (for PWAs)
    bubblewrap_cmd = [
        "npx", "@bubblewrap/cli", "build",
        "--directory", source,
        "--output", output_dir,
    ]
    
    activity.heartbeat("Running Bubblewrap...")
    
    process = await asyncio.create_subprocess_exec(
        *bubblewrap_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    
    stdout, stderr = await process.communicate()
    
    logs.append(stdout.decode())
    if stderr:
        logs.append(stderr.decode())
    
    # Find the APK in output
    output_files = list(Path(output_dir).glob("*.apk"))
    if output_files:
        apk_path = str(output_files[0])
        file_size = Path(apk_path).stat().st_size
        return {
            "success": True,
            "output_path": apk_path,
            "file_size": file_size,
        }
    
    # Bubblewrap failed, try Gradle if manifest exists
    gradle_path = Path(source) / "gradlew"
    if gradle_path.exists():
        activity.heartbeat("Falling back to Gradle...")
        
        gradle_cmd = ["./gradlew", "assembleRelease"]
        process = await asyncio.create_subprocess_exec(
            *gradle_cmd,
            cwd=source,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        
        stdout, stderr = await process.communicate()
        logs.append(stdout.decode())
        
        # Look for APK in build/outputs/apk/release/
        apk_dir = Path(source) / "app" / "build" / "outputs" / "apk" / "release"
        if apk_dir.exists():
            apks = list(apk_dir.glob("*.apk"))
            if apks:
                # Copy to output dir
                dest = Path(output_dir) / apks[0].name
                shutil.copy(apks[0], dest)
                return {
                    "success": True,
                    "output_path": str(dest),
                    "file_size": dest.stat().st_size,
                }
    
    return {
        "success": False,
        "error": "No APK generated",
    }


async def _build_web(source, resources, logs):
    """Build a web app."""
    output_dir = resources["output_dir"]
    
    # Detect build tool
    if (Path(source) / "package.json").exists():
        activity.heartbeat("Running npm build...")
        
        # Install deps
        process = await asyncio.create_subprocess_exec(
            "npm", "ci",
            cwd=source,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        logs.append(stdout.decode())
        
        # Build
        process = await asyncio.create_subprocess_exec(
            "npm", "run", "build",
            cwd=source,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        logs.append(stdout.decode())
        
        # Find dist/build folder
        for dist_name in ["dist", "build", "out"]:
            dist_path = Path(source) / dist_name
            if dist_path.exists():
                # Copy to output
                dest = Path(output_dir) / dist_name
                shutil.copytree(dist_path, dest, dirs_exist_ok=True)
                
                # Calculate total size
                total_size = sum(f.stat().st_size for f in dest.rglob("*") if f.is_file())
                
                return {
                    "success": True,
                    "output_path": str(dest),
                    "file_size": total_size,
                }
    
    # Simple static site - just copy
    activity.heartbeat("Copying static files...")
    dest = Path(output_dir) / "site"
    shutil.copytree(source, dest, dirs_exist_ok=True)
    total_size = sum(f.stat().st_size for f in dest.rglob("*") if f.is_file())
    
    return {
        "success": True,
        "output_path": str(dest),
        "file_size": total_size,
    }


async def _build_docker(source, project, resources, logs):
    """Build a Docker image."""
    tag = f"darkfactory/{project}:{datetime.utcnow().strftime('%Y%m%d')}"
    
    activity.heartbeat(f"Building Docker image {tag}...")
    
    process = await asyncio.create_subprocess_exec(
        "docker", "build", "-t", tag, ".",
        cwd=source,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    
    stdout, stderr = await process.communicate()
    logs.append(stdout.decode())
    
    if process.returncode == 0:
        # Get image size
        size_process = await asyncio.create_subprocess_exec(
            "docker", "images", tag, "--format", "{{.Size}}",
            stdout=asyncio.subprocess.PIPE,
        )
        size_out, _ = await size_process.communicate()
        
        return {
            "success": True,
            "output_path": tag,
            "file_size": 0,  # Parse from docker output if needed
        }
    
    return {
        "success": False,
        "error": stderr.decode(),
    }


@activity.defn
async def verify_build_output(output_path: str, expected_size: int) -> bool:
    """
    Verify that the build output actually exists and has content.
    Patricia's #1 rule: "44 done, 0 files" is NOT okay.
    """
    activity.logger.info(f"Verifying output at {output_path}")
    
    if not output_path:
        activity.logger.error("No output path provided")
        return False
    
    path = Path(output_path)
    
    # Must exist
    if not path.exists():
        activity.logger.error(f"Output does not exist: {output_path}")
        return False
    
    # Must have size > 0
    if path.is_file():
        size = path.stat().st_size
        if size == 0:
            activity.logger.error(f"Output file is empty: {output_path}")
            return False
        activity.logger.info(f"Verified file: {size} bytes")
        return True
    
    elif path.is_dir():
        # Directory must contain files
        files = list(path.rglob("*"))
        files = [f for f in files if f.is_file()]
        if not files:
            activity.logger.error(f"Output directory is empty: {output_path}")
            return False
        total_size = sum(f.stat().st_size for f in files)
        activity.logger.info(f"Verified directory: {len(files)} files, {total_size} bytes")
        return True
    
    return False


@activity.defn
async def validate_hold_out(project_name: str, output_path: str, file_size_bytes: int) -> dict:
    """
    Blind hold-out validation. Runs BEFORE notify_completion.

    SEPARATION RULE (RiP GoR Council, 2026-08-18):
    This activity is the VALIDATOR session. It is intentionally blind to the
    build plan and builder logs. It reads ONLY the pre-authored hold-out
    scenarios + the built output. The builder (execute_build) never sees
    the scenarios; this validator never sees the plan. No shared context = no bias.
    """
    activity.logger.info(f"Running blind hold-out validation for {project_name}")

    try:
        # Import the shared validator (lives in DARK_FACTORY/validation/)
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "hold_out_scenarios",
            "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/validation/hold_out_scenarios.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        result = mod.validate_hold_out(project_name, output_path, file_size_bytes)
        activity.logger.info(
            f"Hold-out result for {project_name}: passed={result.get('passed')} "
            f"score={result.get('score')} ({result.get('passed_count')}/{result.get('total_count')})"
        )
        return result

    except Exception as e:
        # Validation harness itself failing is a config error, not a silent pass.
        activity.logger.error(f"Hold-out validation errored: {e}")
        return {
            "product": project_name,
            "passed": False,
            "score": 0.0,
            "results": [],
            "reason": f"VALIDATOR_ERROR: {e}",
        }


@activity.defn
async def notify_completion(order_id: str, result: dict) -> None:
    """Send completion notification."""
    activity.logger.info(f"Order {order_id} completed: {result}")
    
    # Could send to Discord, Telegram, email, etc.
    # For now, just log
    print(f"✅ DARK FACTORY: {order_id} COMPLETE")
    print(f"   Output: {result.get('output_path')}")
    print(f"   Size: {result.get('file_size_bytes', 0)} bytes")


@activity.defn
async def notify_escalation(order_id: str, stage: str, reason: str) -> None:
    """Escalate stuck or failed builds."""
    activity.logger.error(f"ESCALATION: {order_id} stuck at {stage}: {reason}")
    
    # This is where you'd:
    # - Send Discord alert
    # - Create PagerDuty incident
    # - Notify Captain directly
    print(f"🚨 DARK FACTORY ESCALATION: {order_id}")
    print(f"   Stage: {stage}")
    print(f"   Reason: {reason}")


@activity.defn
async def cleanup_resources(order_id: str) -> None:
    """Clean up build workspace."""
    activity.logger.info(f"Cleaning up resources for {order_id}")
    
    # Find and remove workspace directories
    import glob
    workspaces = glob.glob(f"/tmp/darkfactory/{order_id}_*")
    for ws in workspaces:
        try:
            shutil.rmtree(ws)
            activity.logger.info(f"Removed workspace: {ws}")
        except Exception as e:
            activity.logger.warning(f"Failed to remove {ws}: {e}")