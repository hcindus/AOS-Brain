#!/bin/bash
# Create CREAM Real Estate Android Project v1.1

PROJECT_DIR="/root/.openclaw/workspace/mobile_projects/cream"
mkdir -p $PROJECT_DIR

cd $PROJECT_DIR

mkdir -p app/src/main/java/com/agi/cream/{properties,clients,schedule,documents,calculator,ui}
mkdir -p app/src/main/res/{layout,values,drawable}

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
rootProject.name = "CREAM Real Estate"
EOF

cat > app/build.gradle << 'EOF'
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
    id 'kotlin-kapt'
}
android {
    namespace 'com.agi.cream'
    compileSdk 34
    defaultConfig {
        applicationId "com.agi.cream"
        minSdk 26
        targetSdk 34
        versionCode 11
        versionName "1.1-standalone"
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
    implementation 'androidx.recyclerview:recyclerview:1.3.2'
    implementation 'androidx.cardview:cardview:1.0.0'
    implementation 'androidx.room:room-runtime:2.6.1'
    kapt 'androidx.room:room-compiler:2.6.1'
    implementation 'com.github.bumptech.glide:glide:4.16.0'
    implementation 'androidx.lifecycle:lifecycle-viewmodel-ktx:2.7.0'
    testImplementation 'junit:junit:4.13.2'
}
EOF

cat > app/src/main/AndroidManifest.xml << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.agi.cream">
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.CAMERA" />
    
    <application
        android:name=".CREAMApplication"
        android:allowBackup="false"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/Theme.CREAM">
        
        <activity android:name=".ui.MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        
        <activity android:name=".ui.PropertyListActivity" />
        <activity android:name=".ui.ClientActivity" />
        <activity android:name=".ui.ScheduleActivity" />
        
        <activity android:name=".ui.CalculatorActivity" />
        
    </application>
</manifest>
EOF

echo "CREAM project created at $PROJECT_DIR"
