#!/bin/bash
# Android SDK Environment Setup
# Source this file: source /root/.openclaw/workspace/scripts/setup_android_sdk.sh

export ANDROID_SDK_ROOT=/opt/android-sdk
export ANDROID_HOME=/opt/android-sdk
export PATH=$PATH:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin
export PATH=$PATH:$ANDROID_SDK_ROOT/platform-tools
export PATH=$PATH:$ANDROID_SDK_ROOT/build-tools/34.0.0

echo "✅ Android SDK environment configured"
echo "   ANDROID_SDK_ROOT: $ANDROID_SDK_ROOT"
echo "   SDK Version: $($ANDROID_SDK_ROOT/cmdline-tools/latest/bin/sdkmanager --version 2>/dev/null || echo 'N/A')"
