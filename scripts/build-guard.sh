#!/bin/bash
# Build Guard - Wrap builds with resource checks and cleanup

PROJECT_NAME="$1"
BUILD_CMD="$2"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JOB_QUEUE="$SCRIPT_DIR/job-queue.sh"
RESOURCE_GUARD="$SCRIPT_DIR/resource-guard.sh"

if [[ -z "$PROJECT_NAME" || -z "$BUILD_CMD" ]]; then
    echo "Usage: $0 <project-name> '<build-command>'"
    exit 1
fi

# Strict resource check for builds
if ! "$RESOURCE_GUARD" 50 2.0; then
    echo "Resources too busy for build, queuing $PROJECT_NAME..."
    "$JOB_QUEUE" queue "$PROJECT_NAME-build" "$BUILD_CMD" high
    exit 0
fi

# Queue and run with cleanup trap
"$JOB_QUEUE" queue "$PROJECT_NAME-build" "$BUILD_CMD" high

# Set trap to kill Gradle/Java on exit
cleanup() {
    echo "Build interrupted, cleaning up..."
    pkill -f "GradleDaemon" 2>/dev/null
    pkill -f "java.*$PROJECT_NAME" 2>/dev/null
    "$JOB_QUEUE" cleanup
}
trap cleanup EXIT INT TERM

"$JOB_QUEUE" run
exit_code=$?

# Explicit cleanup
cleanup

echo "Build completed with exit code $exit_code"
exit $exit_code
