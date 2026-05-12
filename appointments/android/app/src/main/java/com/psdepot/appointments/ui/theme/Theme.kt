package com.psdepot.appointments.ui.theme

import android.app.Activity
import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

private val DarkColorScheme = darkColorScheme(
    primary = PSDBlue,
    onPrimary = Color.Black,
    primaryContainer = PSDBlue.copy(alpha = 0.2f),
    onPrimaryContainer = PSDBlue,
    secondary = PSDOrange,
    onSecondary = Color.Black,
    secondaryContainer = PSDOrange.copy(alpha = 0.2f),
    onSecondaryContainer = PSDOrange,
    tertiary = Color(0xFF9C27B0),
    onTertiary = Color.White,
    tertiaryContainer = Color(0xFF7B1FA2),
    onTertiaryContainer = Color(0xFFE1BEE7),
    background = DarkBackground,
    onBackground = DarkOnBackground,
    surface = DarkSurface,
    onSurface = DarkOnSurface,
    surfaceVariant = DarkSurfaceVariant,
    onSurfaceVariant = DarkOnSurfaceVariant,
    error = PSDError,
    onError = Color.White,
    errorContainer = PSDError.copy(alpha = 0.2f),
    onErrorContainer = PSDError,
    outline = DarkOutline,
    outlineVariant = DarkOutline.copy(alpha = 0.5f),
    inverseSurface = DarkOnBackground,
    inverseOnSurface = DarkBackground,
    inversePrimary = PSDBlue.copy(alpha = 0.8f),
    scrim = Color.Black.copy(alpha = 0.6f)
)

private val LightColorScheme = lightColorScheme(
    primary = PSDBlue,
    onPrimary = Color.White,
    primaryContainer = PSDBlue.copy(alpha = 0.1f),
    onPrimaryContainer = PSDBlue,
    secondary = PSDOrange,
    onSecondary = Color.White,
    secondaryContainer = PSDOrange.copy(alpha = 0.1f),
    onSecondaryContainer = PSDOrange,
    tertiary = Color(0xFF7B1FA2),
    onTertiary = Color.White,
    tertiaryContainer = Color(0xFFE1BEE7),
    onTertiaryContainer = Color(0xFF4A148C),
    background = Color(0xFFF5F5FA),
    onBackground = Color(0xFF1A1A2E),
    surface = Color.White,
    onSurface = Color(0xFF1A1A2E),
    surfaceVariant = Color(0xFFF0F0F5),
    onSurfaceVariant = Color(0xFF4A4A5A),
    error = Color(0xFFB00020),
    onError = Color.White,
    errorContainer = Color(0xFFFFDAD6),
    onErrorContainer = Color(0xFF410002),
    outline = Color(0xFF79747E),
    outlineVariant = Color(0xFFCAC4D0)
)

@Composable
fun PSDAppointmentsTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = false, // Disabled by default for consistent PSD branding
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }
        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }
    
    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val window = (view.context as Activity).window
            window.statusBarColor = colorScheme.background.toArgb()
            WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = !darkTheme
        }
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = PSDTypography,
        content = content
    )
}
