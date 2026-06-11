package com.psdepot.appointments.ui.theme

import androidx.compose.ui.graphics.Color

// PSD Brand Colors
val PSDDark = Color(0xFF0A0A1A)
val PSDDarkSecondary = Color(0xFF121228)
val PSDDarkTertiary = Color(0xFF1A1A3E)

val PSDCyan = Color(0xFF00E0FF)
val PSDCyanDim = Color(0x1A00E0FF)
val PSDCyanGlow = Color(0x4D00E0FF)

val PSDOrange = Color(0xFFFF7A00)
val PSDOrangeDim = Color(0x1AFF7A00)
val PSDOrangeGlow = Color(0x4DFF7A00)

// Semantic Colors
val BackgroundPrimary = PSDDark
val BackgroundSecondary = PSDDarkSecondary
val BackgroundTertiary = PSDDarkTertiary
val BackgroundInput = Color(0x0DFFFFFF)

val TextPrimary = Color.White
val TextSecondary = Color.White.copy(alpha = 0.8f)
val TextMuted = Color.White.copy(alpha = 0.5f)
val TextPlaceholder = Color.White.copy(alpha = 0.3f)

val BorderDefault = Color.White.copy(alpha = 0.1f)
val BorderFocus = PSDCyan

// Status Colors
val ErrorColor = Color(0xFFFF4757)
val ErrorBackground = Color(0x1AFF4757)
val SuccessColor = Color(0xFF2ED573)
val SuccessBackground = Color(0x1A2ED573)
val WarningColor = Color(0xFFFFA502)
val WarningBackground = Color(0x1AFFA502)