#!/bin/bash
# Patricia Factory Controller v2.0 - Cron Job
# Executes factory tick every 5 minutes

export ANDROID_SDK_ROOT=/opt/android-sdk
export ANDROID_HOME=/opt/android-sdk
export PATH=$PATH:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$ANDROID_SDK_ROOT/platform-tools

cd /root/.openclaw/workspace/agent_sandboxes/patricia
/usr/bin/python3 patricia_factory_controller_v2.py tick >> /var/log/aos/patricia_factory_v2.log 2>&1
