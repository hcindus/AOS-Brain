// PSD Appointments - Android App
// 
// This is the Android mobile application for the PSD Appointment Scheduling System.
// It provides a complete mobile experience for managing appointments, searching leads,
// and scheduling consultations.
//
// Architecture:
// - MVVM pattern with Jetpack Compose
// - Hilt for dependency injection
// - Room for offline persistence
// - Retrofit for API communication
// - Firebase Cloud Messaging for push notifications
//
// Features:
// 1. Sentinel-Dusty authentication integration
// 2. Adaptive calendar (mobile + tablet/desktop layouts)
// 3. Real-time availability and booking
// 4. Leads search from DepotChaos
// 5. Offline support with Room database
// 6. Push notifications via FCM
//
// Branding:
// - Dark theme with PSD cyan (#00E0FF) and orange (#FF7A00) accents
// - Modern Material Design 3 components
//
// Backend API:
// - Base URL: http://10.0.2.2:8083/ (Android Emulator) or production endpoint
// - Port: 8083
// - Authentication: JWT via Sentinel-Dusty

package com.psdepot.appointments

// Root package marker
