# Android SDK Environment Configuration
# Source this file: source /root/.openclaw/workspace/scripts/android-sdk-env.sh

export ANDROID_SDK_ROOT=/opt/android-sdk
export ANDROID_HOME=/opt/android-sdk
export PATH=$PATH:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin
export PATH=$PATH:$ANDROID_SDK_ROOT/platform-tools
export PATH=$PATH:$ANDROID_SDK_ROOT/build-tools/34.0.0
export PATH=$PATH:$ANDROID_SDK_ROOT/tools/bin

# Verify
echo "Android SDK: $ANDROID_SDK_ROOT"
echo "Build Tools: $(ls $ANDROID_SDK_ROOT/build-tools/ | tail -1)"
