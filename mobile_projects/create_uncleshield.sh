#!/bin/bash
# Create UncleShield AV Android Project v4.0

PROJECT_DIR="/root/.openclaw/workspace/mobile_projects/uncleshield-av"
mkdir -p $PROJECT_DIR

cd $PROJECT_DIR

mkdir -p app/src/main/java/com/agi/uncleshield/{scanner,protection,database,ui,utils}
mkdir -p app/src/main/res/{layout,values,drawable,mipmap-hdpi,mipmap-mdpi,mipmap-xhdpi,mipmap-xxhdpi,mipmap-xxxhdpi}

# build.gradle (Project)
cat > build.gradle << 'EOF'
buildscript {
    ext.kotlin_version = '1.9.0'
    repositories { google(); mavenCentral() }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.1.0'
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"
    }
}
allprojects { repositories { google(); mavenCentral() } }
EOF

cat > settings.gradle << 'EOF'
include ':app'
rootProject.name = "UncleShield AV"
EOF

cat > app/build.gradle << 'EOF'
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}
android {
    namespace 'com.agi.uncleshield'
    compileSdk 34
    defaultConfig {
        applicationId "com.agi.uncleshield"
        minSdk 26
        targetSdk 34
        versionCode 40
        versionName "4.0-polished"
    }
    buildTypes {
        release {
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = '17' }
}
dependencies {
    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    implementation 'androidx.work:work-runtime-ktx:2.9.0'
    implementation 'androidx.lifecycle:lifecycle-service:2.7.0'
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3'
    testImplementation 'junit:junit:4.13.2'
}
EOF

cat > app/src/main/AndroidManifest.xml << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.agi.uncleshield">
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.RECEIVE_SMS" />
    <uses-permission android:name="android.permission.READ_SMS" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    
    <application
        android:allowBackup="false"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/Theme.UncleShield"
        android:name=".UncleShieldApplication">
        
        <activity android:name=".ui.MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        
        <service android:name=".scanner.RealTimeProtectionService"
            android:foregroundServiceType="dataSync" />
            
        <receiver android:name=".protection.SmsScamDetector"
            android:exported="true">
            <intent-filter>
                <action android:name="android.provider.Telephony.SMS_RECEIVED" />
            </intent-filter>
        </receiver>
        
    </application>
</manifest>
EOF

echo "UncleShield AV project created at $PROJECT_DIR"
