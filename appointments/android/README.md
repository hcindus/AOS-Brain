# PSD Appointments - Android

A modern Android application for the PSD Appointment Scheduling System.

## Features

- **Authentication**: Integrated with Sentinel-Dusty auth API
- **Adaptive Calendar**: Mobile-optimized and tablet/desktop layouts
- **Booking Flow**: Select slots, enter details, confirm appointments
- **Leads Search**: Integration with DepotChaos leads database
- **Offline Support**: Room database for persistence
- **Push Notifications**: FCM integration for real-time updates

## Tech Stack

- **Language**: Kotlin
- **UI**: Jetpack Compose with Material Design 3
- **Architecture**: MVVM
- **DI**: Hilt
- **Database**: Room
- **Networking**: Retrofit + OkHttp
- **Async**: Kotlin Coroutines + Flow
- **Notifications**: Firebase Cloud Messaging

## Branding

- **Primary**: Cyan #00E0FF
- **Secondary**: Orange #FF7A00
- **Background**: Dark #0A0A0F
- **Theme**: Dark mode optimized

## Building

```bash
./gradlew assembleDebug
```

## Configuration

The app connects to the appointments backend on port 8083.
For Android Emulator, use `10.0.2.2:8083`.
