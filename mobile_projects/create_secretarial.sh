#!/bin/bash
# Create Secretarial Pool Products Android Project v1.0

PROJECT_DIR="/root/.openclaw/workspace/mobile_projects/secretarial-pool"
mkdir -p $PROJECT_DIR

cd $PROJECT_DIR

mkdir -p app/src/main/java/com/agi/secretarial/{admin,documents,tasks,ui}
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
rootProject.name = "Secretarial Pool"
EOF

cat > app/build.gradle << 'EOF'
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}
android {
    namespace 'com.agi.secretarial'
    compileSdk 34
    defaultConfig {
        applicationId "com.agi.secretarial"
        minSdk 26
        targetSdk 34
        versionCode 10
        versionName "1.0-standalone"
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
    implementation 'androidx.work:work-runtime-ktx:2.9.0'
    testImplementation 'junit:junit:4.13.2'
}
EOF

cat > app/src/main/AndroidManifest.xml << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.agi.secretarial">
    
    <uses-permission android:name="android.permission.INTERNET" />
    
    <application
        android:name=".SecretarialApplication"
        android:allowBackup="false"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/Theme.Secretarial">
        
        <activity android:name=".ui.MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        
        <activity android:name=".admin.AdminActivity" />
        <activity android:name=".documents.DocumentsActivity" />
        <activity android:name=".tasks.TasksActivity" />
        
    </application>
</manifest>
EOF

echo "Secretarial Pool project created at $PROJECT_DIR"
