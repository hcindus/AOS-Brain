#!/bin/bash
# Create Performance Supply Depot POS Supplies Android Project v1.0

PROJECT_DIR="/root/.openclaw/workspace/mobile_projects/psdepot-supplies"
mkdir -p $PROJECT_DIR

cd $PROJECT_DIR

mkdir -p app/src/main/java/com/agi/psdepot/{supplies,catalog,orders,ui}
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
rootProject.name = "PS Depot Supplies"
EOF

cat > app/build.gradle << 'EOF'
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}
android {
    namespace 'com.agi.psdepot'
    compileSdk 34
    defaultConfig {
        applicationId "com.agi.psdepot"
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
    implementation 'androidx.cardview:cardview:1.0.0'
    testImplementation 'junit:junit:4.13.2'
}
EOF

cat > app/src/main/AndroidManifest.xml << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.agi.psdepot">
    
    <uses-permission android:name="android.permission.INTERNET" />
    
    <application
        android:name=".PSDepotApplication"
        android:allowBackup="false"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/Theme.PSDepot">
        
        <activity android:name=".ui.MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        
        <activity android:name=".catalog.CatalogActivity" />
        <activity android:name=".orders.OrderActivity" />
        <activity android:name=".supplies.SuppliesActivity" />
        
    </application>
</manifest>
EOF

echo "PS Depot Supplies project created at $PROJECT_DIR"
