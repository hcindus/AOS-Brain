#!/usr/bin/env python3
"""
COBRA Assembly Animation System
Step-by-step 3D animated build instructions
Generates HTML/CSS/JS for web viewing
"""

import json
from dataclasses import dataclass
from typing import List, Dict, Tuple
from enum import Enum


class AssemblyStepType(Enum):
    PREPARE = "prepare"
    ATTACH = "attach"
    CONNECT = "connect"
    TEST = "test"
    CALIBRATE = "calibrate"


@dataclass
class AssemblyStep:
    """Single assembly step"""
    step_number: int
    title: str
    description: str
    step_type: str
    parts_needed: List[str]
    tools_needed: List[str]
    duration_minutes: int
    difficulty: str  # Easy, Medium, Hard
    warnings: List[str]
    
    # 3D visualization data
    camera_position: Tuple[float, float, float]
    highlight_parts: List[str]
    show_previous: bool
    animation_script: str


class AssemblyAnimator:
    """Generate animated assembly instructions"""
    
    def __init__(self):
        self.steps: List[AssemblyStep] = []
        self.current_step = 0
        
    def generate_full_assembly(self):
        """Generate complete assembly sequence"""
        
        # PHASE 1: PREPARATION
        self.steps.append(AssemblyStep(
            1, "Prepare Workspace",
            "Clear workspace, organize tools, verify all parts from BOM",
            AssemblyStepType.PREPARE.value,
            ["TLS-001", "TLS-002", "TLS-003"],
            ["Work mat", "Tweezers", "Magnifying glass"],
            15, "Easy",
            ["Work on ESD mat", "Keep screws sorted by size"],
            (0, 10, 10), [], False,
            "workspace_setup"
        ))
        
        self.steps.append(AssemblyStep(
            2, "Print Verification",
            "Inspect all 3D printed parts for defects. Check layer adhesion and dimensions",
            AssemblyStepType.PREPARE.value,
            ["STR-001", "STR-002", "STR-003", "STR-004", "STR-006", "STR-007"],
            [],
            20, "Easy",
            ["Reject parts with layer separation", "Smooth rough edges with sandpaper"],
            (5, 5, 5), ["STR-001", "STR-002", "STR-003", "STR-004", "STR-006", "STR-007"], False,
            "parts_explode"
        ))
        
        # PHASE 2: VERTEBRA ASSEMBLY
        self.steps.append(AssemblyStep(
            3, "Prepare Servo Mounts",
            "Install servo horns into each vertebra. Ensure 90° center position",
            AssemblyStepType.PREPARE.value,
            ["ACT-001", "ACT-002", "FAS-005", "FAS-006"],
            ["Screwdriver"],
            30, "Medium",
            ["Do NOT power servos yet", "Horns should rotate freely"],
            (2, 2, 3), ["STR-001"], False,
            "servo_insert"
        ))
        
        self.steps.append(AssemblyStep(
            4, "Assemble Cervical Spine (V1-V7)",
            "Connect first 7 vertebrae. Install pitch servos and intervertebral discs",
            AssemblyStepType.ATTACH.value,
            ["STR-001", "ACT-001", "STR-005", "FAS-001", "FAS-003"],
            ["Screwdriver", "Tweezers"],
            45, "Medium",
            ["Keep servo wires organized", "Test each joint manually"],
            (0, 0, 2), ["STR-001"], True,
            "vertebra_stack"
        ))
        
        self.steps.append(AssemblyStep(
            5, "Add Roll Joints to Cervical",
            "Install roll servos perpendicular to pitch axis for lateral movement",
            AssemblyStepType.ATTACH.value,
            ["ACT-002", "FAS-001", "FAS-003"],
            ["Screwdriver"],
            30, "Hard",
            ["Orientation is critical - check diagram", "Roll axis must be truly perpendicular"],
            (1, 1, 2), ["STR-001"], True,
            "roll_servo_install"
        ))
        
        self.steps.append(AssemblyStep(
            6, "Assemble Thoracic Spine (V8-V19)",
            "Build middle section with rib attachments. Less flexible but more stable",
            AssemblyStepType.ATTACH.value,
            ["STR-002", "STR-006", "ACT-001", "ACT-002", "FAS-001"],
            ["Screwdriver"],
            60, "Medium",
            ["Ribs attach to thoracic only", "Maintain natural kyphosis curve"],
            (0, 0, 1.5), ["STR-001", "STR-002"], True,
            "thoracic_build"
        ))
        
        self.steps.append(AssemblyStep(
            7, "Assemble Lumbar Spine (V20-V24)",
            "Build lower back section with increased flexibility for balance",
            AssemblyStepType.ATTACH.value,
            ["STR-003", "ACT-001", "ACT-002", "STR-005"],
            ["Screwdriver"],
            35, "Medium",
            ["More flexible than thoracic", "Prepare for sacrum attachment"],
            (0, 0, 1), ["STR-001", "STR-002", "STR-003"], True,
            "lumbar_build"
        ))
        
        self.steps.append(AssemblyStep(
            8, "Attach Sacrum Base",
            "Install rigid base plate with high-torque servos for hip joints",
            AssemblyStepType.ATTACH.value,
            ["STR-004", "ACT-003", "FAS-001", "FAS-002"],
            ["Screwdriver", "Threadlocker"],
            25, "Medium",
            ["Use threadlocker on base screws", "Verify 0.5mm clearance"],
            (0, 0, 0.5), ["STR-001", "STR-002", "STR-003", "STR-004"], True,
            "sacrum_attach"
        ))
        
        # PHASE 3: ELECTRONICS
        self.steps.append(AssemblyStep(
            9, "Install Brain (Raspberry Pi)",
            "Mount Pi 5 in skull housing with AI HAT and cooling",
            AssemblyStepType.ATTACH.value,
            ["ELE-001", "ELE-002", "ELE-006", "ELE-007"],
            ["Thermal paste", "Screwdriver"],
            20, "Medium",
            ["Apply thermal paste sparingly", "Fan must clear housing by 2mm"],
            (2, 2, 4), ["STR-007", "ELE-001"], True,
            "brain_install"
        ))
        
        self.steps.append(AssemblyStep(
            10, "Wire Servo Controllers",
            "Install PCA9685 boards and route all servo cables",
            AssemblyStepType.CONNECT.value,
            ["ELE-003", "CBL-001", "CBL-002", "FAS-001"],
            ["Wire stripper", "Crimping tool"],
            60, "Hard",
            ["Label EVERY wire", "Route in spiral pattern down spine", "Keep high-current away from signal"],
            (1, 1, 3), ["STR-001", "ELE-003"], True,
            "servo_wiring"
        ))
        
        self.steps.append(AssemblyStep(
            11, "Install IMU Sensors",
            "Mount MPU6050 units at skull and sacrum for balance feedback",
            AssemblyStepType.ATTACH.value,
            ["SEN-001", "CBL-003", "FAS-001"],
            ["Hot glue gun", "Screwdriver"],
            15, "Medium",
            ["Align IMU Z-axis with spine", "Secure cables with zip ties"],
            (2, 0, 3), ["STR-007", "STR-004", "SEN-001"], True,
            "imu_mount"
        ))
        
        self.steps.append(AssemblyStep(
            12, "Install Distance Sensors",
            "Add ToF and IR sensors to skull for obstacle detection",
            AssemblyStepType.ATTACH.value,
            ["SEN-002", "SEN-004", "FAS-001"],
            ["Drill", "File"],
            20, "Medium",
            ["ToF sensor faces forward", "IR sensors at 45° angles"],
            (2.5, 0, 4), ["STR-007", "SEN-002"], True,
            "sensor_mount"
        ))
        
        # PHASE 4: POWER
        self.steps.append(AssemblyStep(
            13, "Assemble Battery Pack",
            "Build 3S2P 18650 pack with BMS protection",
            AssemblyStepType.PREPARE.value,
            ["PWR-001", "PWR-002", "PWR-006"],
            ["Spot welder", "Multimeter"],
            45, "Hard",
            ["VERIFY POLARITY", "Test each cell voltage", "BMS must connect last"],
            (3, 3, 0), ["PWR-006"], False,
            "battery_build"
        ))
        
        self.steps.append(AssemblyStep(
            14, "Install Power Distribution",
            "Mount buck converter, switches, and current sensors",
            AssemblyStepType.CONNECT.value,
            ["PWR-003", "PWR-004", "PWR-005", "SEN-005"],
            ["Soldering iron", "Heat shrink"],
            40, "Hard",
            ["Fuse servo power separately", "Add power switch accessible from outside"],
            (2, 2, 0.5), ["STR-004", "PWR-003"], True,
            "power_install"
        ))
        
        # PHASE 5: FINAL ASSEMBLY
        self.steps.append(AssemblyStep(
            15, "Connect All Wiring",
            "Final wiring harness connection to brain and controllers",
            AssemblyStepType.CONNECT.value,
            ["CBL-002", "CBL-004", "CBL-005", "CBL-006"],
            ["Cable ties", "Heat gun"],
            30, "Medium",
            ["Double-check all connections", "No pinching when spine bends"],
            (1, 1, 2), [], True,
            "final_wiring"
        ))
        
        self.steps.append(AssemblyStep(
            16, "Install Phone Mount",
            "Attach adjustable phone holder to skull",
            AssemblyStepType.ATTACH.value,
            ["STR-008", "FAS-001"],
            ["Screwdriver"],
            10, "Easy",
            ["Verify phone fits before finalizing", "Leave access to Pi ports"],
            (2, 0, 4), ["STR-007", "STR-008"], True,
            "phone_mount"
        ))
        
        # PHASE 6: TESTING
        self.steps.append(AssemblyStep(
            17, "Power-On Test",
            "First power-up: check voltages, verify no smoke",
            AssemblyStepType.TEST.value,
            [],
            ["Multimeter", "Smoke detector"],
            10, "Medium",
            ["Have fire extinguisher ready", "Check 5V rail first", "Feel for hot spots"],
            (3, 3, 2), [], True,
            "power_test"
        ))
        
        self.steps.append(AssemblyStep(
            18, "Servo Calibration",
            "Set all servos to 90° neutral, verify range of motion",
            AssemblyStepType.CALIBRATE.value,
            [],
            ["Laptop", "USB cable"],
            30, "Medium",
            ["Move ONE servo at a time", "Check for mechanical binding", "Record offset values"],
            (1, 1, 3), [], True,
            "servo_calibrate"
        ))
        
        self.steps.append(AssemblyStep(
            19, "Balance System Test",
            "Verify IMU readings and balance control loop",
            AssemblyStepType.TEST.value,
            [],
            ["Laptop"],
            20, "Hard",
            ["Robot must be on stable surface", "Test pitch then roll separately"],
            (2, 0, 2), [], True,
            "balance_test"
        ))
        
        self.steps.append(AssemblyStep(
            20, "Full System Integration",
            "Run complete diagnostic, test all functions",
            AssemblyStepType.TEST.value,
            [],
            ["Laptop", "Test stand"],
            45, "Hard",
            ["Secure to test stand first", "Test walking in place", "Verify emergency stop works"],
            (0, 0, 2), [], True,
            "full_test"
        ))
        
    def generate_html(self, filename: str = "COBRA_Assembly_Guide.html"):
        """Generate interactive HTML assembly guide"""
        
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>COBRA Robot - Assembly Guide</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0a0f;
            color: #e0e0e0;
            line-height: 1.6;
        }
        .header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 2rem;
            text-align: center;
            border-bottom: 3px solid #00d4aa;
        }
        .header h1 { color: #00d4aa; font-size: 2.5rem; margin-bottom: 0.5rem; }
        .header p { color: #888; }
        .container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
        .progress-bar {
            background: #1a1a2e;
            height: 8px;
            border-radius: 4px;
            margin: 2rem 0;
            overflow: hidden;
        }
        .progress-fill {
            background: linear-gradient(90deg, #00d4aa, #00a884);
            height: 100%;
            width: 0%;
            transition: width 0.5s ease;
        }
        .step-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            margin: 2rem 0;
        }
        .step-info {
            background: #151520;
            border-radius: 12px;
            padding: 2rem;
            border: 1px solid #2a2a3e;
        }
        .step-number {
            display: inline-block;
            background: #00d4aa;
            color: #0a0a0f;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            text-align: center;
            line-height: 40px;
            font-weight: bold;
            font-size: 1.2rem;
            margin-bottom: 1rem;
        }
        .step-title { font-size: 1.5rem; color: #fff; margin-bottom: 1rem; }
        .step-description { color: #aaa; margin-bottom: 1.5rem; }
        .meta-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        .meta-item {
            background: #0f0f1a;
            padding: 0.75rem;
            border-radius: 8px;
            text-align: center;
        }
        .meta-label { font-size: 0.75rem; color: #666; text-transform: uppercase; }
        .meta-value { font-size: 1.1rem; color: #00d4aa; font-weight: bold; }
        .parts-list, .tools-list, .warnings-list {
            margin-top: 1rem;
        }
        .list-title {
            font-size: 0.875rem;
            color: #888;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }
        .part-tag, .tool-tag {
            display: inline-block;
            background: #1e3a5f;
            color: #64b5f6;
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.85rem;
            margin: 0.25rem;
        }
        .warning-item {
            background: #3a1f1f;
            border-left: 3px solid #ff6b6b;
            padding: 0.75rem;
            margin: 0.5rem 0;
            border-radius: 0 8px 8px 0;
        }
        .viewer-3d {
            background: #0d0d15;
            border-radius: 12px;
            border: 1px solid #2a2a3e;
            min-height: 500px;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .viewer-placeholder {
            text-align: center;
            color: #444;
        }
        .viewer-placeholder .icon {
            font-size: 4rem;
            margin-bottom: 1rem;
        }
        .controls {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 2rem;
        }
        .btn {
            background: #1a1a2e;
            border: 2px solid #00d4aa;
            color: #00d4aa;
            padding: 1rem 2rem;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .btn:hover {
            background: #00d4aa;
            color: #0a0a0f;
        }
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .difficulty-easy { color: #4ade80; }
        .difficulty-medium { color: #fbbf24; }
        .difficulty-hard { color: #f87171; }
        .timeline {
            display: flex;
            justify-content: space-between;
            margin: 2rem 0;
            padding: 0 1rem;
        }
        .timeline-item {
            text-align: center;
            flex: 1;
            position: relative;
        }
        .timeline-dot {
            width: 16px;
            height: 16px;
            background: #333;
            border-radius: 50%;
            margin: 0 auto 0.5rem;
            transition: all 0.3s ease;
        }
        .timeline-item.active .timeline-dot { background: #00d4aa; }
        .timeline-item.completed .timeline-dot { background: #00a884; }
        .timeline-label { font-size: 0.75rem; color: #666; }
        @media (max-width: 768px) {
            .step-container { grid-template-columns: 1fr; }
            .meta-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🐍 COBRA Robot Assembly</h1>
        <p>Step-by-step animated build guide • 20 steps • ~8 hours</p>
    </div>
    
    <div class="container">
        <div class="timeline">
            <div class="timeline-item completed"><div class="timeline-dot"></div><div class="timeline-label">Prep</div></div>
            <div class="timeline-item active"><div class="timeline-dot"></div><div class="timeline-label">Spine</div></div>
            <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-label">Electronics</div></div>
            <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-label">Power</div></div>
            <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-label">Final</div></div>
            <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-label">Test</div></div>
        </div>
        
        <div class="progress-bar">
            <div class="progress-fill" id="progress"></div>
        </div>
        
        <div class="step-container" id="step-content">
"""
        
        # Add steps
        for i, step in enumerate(self.steps):
            active_class = "active" if i == 0 else ""
            difficulty_class = f"difficulty-{step.difficulty.lower()}"
            
            html += f"""
        <div class="step-section" data-step="{step.step_number}" style="display: {'grid' if i == 0 else 'none'};">
            <div class="step-info">
                <span class="step-number">{step.step_number}</span>
                <h2 class="step-title">{step.title}</h2>
                <p class="step-description">{step.description}</p>
                
                <div class="meta-grid">
                    <div class="meta-item">
                        <div class="meta-label">Time</div>
                        <div class="meta-value">{step.duration_minutes}m</div>
                    </div>
                    <div class="meta-item">
                        <div class="meta-label">Difficulty</div>
                        <div class="meta-value {difficulty_class}">{step.difficulty}</div>
                    </div>
                    <div class="meta-item">
                        <div class="meta-label">Type</div>
                        <div class="meta-value">{step.step_type.title()}</div>
                    </div>
                </div>
                
                <div class="parts-list">
                    <div class="list-title">Parts Needed ({len(step.parts_needed)})</div>
                    {''.join(f'<span class="part-tag">{p}</span>' for p in step.parts_needed[:8])}
                    {f'<span class="part-tag">+{len(step.parts_needed) - 8} more</span>' if len(step.parts_needed) > 8 else ''}
                </div>
                
                <div class="tools-list">
                    <div class="list-title">Tools</div>
                    {''.join(f'<span class="tool-tag">{t}</span>' for t in step.tools_needed) if step.tools_needed else '<span style="color: #666;">None</span>'}
                </div>
                
                <div class="warnings-list">
                    <div class="list-title">⚠️ Important</div>
                    {''.join(f'<div class="warning-item">{w}</div>' for w in step.warnings)}
                </div>
            </div>
            
            <div class="viewer-3d">
                <div class="viewer-placeholder">
                    <div class="icon">🎬</div>
                    <p>3D Animation: {step.animation_script}</p>
                    <p style="font-size: 0.85rem; margin-top: 0.5rem;">Camera: {step.camera_position}</p>
                    <p style="font-size: 0.85rem;">Highlight: {', '.join(step.highlight_parts) if step.highlight_parts else 'Full assembly'}</p>
                </div>
            </div>
        </div>
"""
        
        html += """
        </div>
        
        <div class="controls">
            <button class="btn" id="prevBtn" onclick="prevStep()" disabled>← Previous</button>
            <button class="btn" id="nextBtn" onclick="nextStep()">Next →</button>
        </div>
    </div>
    
    <script>
        let currentStep = 1;
        const totalSteps = 20;
        
        function updateStep() {
            // Hide all steps
            document.querySelectorAll('.step-section').forEach(el => {
                el.style.display = 'none';
            });
            
            // Show current step
            const currentEl = document.querySelector(`[data-step="${currentStep}"]`);
            if (currentEl) currentEl.style.display = 'grid';
            
            // Update progress
            const progress = (currentStep / totalSteps) * 100;
            document.getElementById('progress').style.width = progress + '%';
            
            // Update buttons
            document.getElementById('prevBtn').disabled = currentStep === 1;
            document.getElementById('nextBtn').disabled = currentStep === totalSteps;
            document.getElementById('nextBtn').textContent = currentStep === totalSteps ? 'Complete ✓' : 'Next →';
            
            // Update timeline
            document.querySelectorAll('.timeline-item').forEach((el, idx) => {
                el.classList.remove('active', 'completed');
                if (idx < Math.floor((currentStep - 1) / 4)) {
                    el.classList.add('completed');
                } else if (idx === Math.floor((currentStep - 1) / 4)) {
                    el.classList.add('active');
                }
            });
            
            // Save progress
            localStorage.setItem('cobraAssemblyStep', currentStep);
        }
        
        function nextStep() {
            if (currentStep < totalSteps) {
                currentStep++;
                updateStep();
            }
        }
        
        function prevStep() {
            if (currentStep > 1) {
                currentStep--;
                updateStep();
            }
        }
        
        // Load saved progress
        const saved = localStorage.getItem('cobraAssemblyStep');
        if (saved) {
            currentStep = parseInt(saved);
        }
        
        updateStep();
    </script>
</body>
</html>"""
        
        with open(filename, 'w') as f:
            f.write(html)
            
        print(f"✅ Assembly guide exported to {filename}")
        
    def print_assembly_summary(self):
        """Print assembly summary"""
        print("\n" + "=" * 80)
        print("🐍 COBRA Assembly Sequence")
        print("=" * 80)
        
        total_time = sum(s.duration_minutes for s in self.steps)
        
        phases = {
            "Preparation": [],
            "Spine Assembly": [],
            "Electronics": [],
            "Power System": [],
            "Final Assembly": [],
            "Testing": []
        }
        
        for step in self.steps:
            if step.step_number <= 2:
                phases["Preparation"].append(step)
            elif step.step_number <= 8:
                phases["Spine Assembly"].append(step)
            elif step.step_number <= 12:
                phases["Electronics"].append(step)
            elif step.step_number <= 14:
                phases["Power System"].append(step)
            elif step.step_number <= 16:
                phases["Final Assembly"].append(step)
            else:
                phases["Testing"].append(step)
                
        for phase, steps in phases.items():
            if steps:
                phase_time = sum(s.duration_minutes for s in steps)
                hard_steps = sum(1 for s in steps if s.difficulty == "Hard")
                print(f"\n📦 {phase} ({len(steps)} steps, {phase_time} min)")
                if hard_steps:
                    print(f"   ⚠️  {hard_steps} hard difficulty steps")
                for step in steps:
                    icon = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}[step.difficulty]
                    print(f"   {step.step_number:2d}. {icon} {step.title} ({step.duration_minutes}m)")
                    
        print(f"\n⏱️  Total Assembly Time: {total_time // 60}h {total_time % 60}m")
        print(f"   Difficulty Distribution:")
        easy = sum(1 for s in self.steps if s.difficulty == "Easy")
        medium = sum(1 for s in self.steps if s.difficulty == "Medium")
        hard = sum(1 for s in self.steps if s.difficulty == "Hard")
        print(f"      🟢 Easy: {easy} | 🟡 Medium: {medium} | 🔴 Hard: {hard}")


def main():
    """Generate assembly animations"""
    print("🎬 Generating COBRA Assembly Guide...")
    
    animator = AssemblyAnimator()
    animator.generate_full_assembly()
    
    # Print summary
    animator.print_assembly_summary()
    
    # Export HTML
    animator.generate_html()
    
    print("\n" + "=" * 80)
    print("✅ Assembly Guide Complete")
    print("=" * 80)
    print("\nOpen COBRA_Assembly_Guide.html in your browser")
    print("Features:")
    print("  • Step-by-step navigation")
    print("  • Progress tracking (saved to localStorage)")
    print("  • Parts and tools lists per step")
    print("  • Important warnings highlighted")
    print("  • Phase timeline visualization")


if __name__ == "__main__":
    main()
