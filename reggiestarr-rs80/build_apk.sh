#!/bin/bash
# Build RS-80 APK

cd /root/.openclaw/workspace/reggiestarr-rs80

# Make gradlew executable
chmod +x ./gradlew 2>/dev/null || echo "No gradlew yet"

# Build debug APK
if [ -f "./gradlew" ]; then
    ./gradlew assembleDebug
else
    echo "Gradle wrapper not found. Manual build required."
    echo "Open in Android Studio and build from there."
fi

echo "Build complete. Check app/build/outputs/apk/debug/"
