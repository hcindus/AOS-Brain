# ProGuard rules for ReggieStarr RS-80

# Keep Room entities
-keep class com.ps.pos.data.entities.** { *; }

# Keep DAO interfaces
-keep class com.ps.pos.data.dao.** { *; }

# Keep ESC/POS classes
-keep class com.github.anastaciocintra.escpos.coffee.** { *; }

# Keep Compose preview
-keep class androidx.compose.runtime.Composable { *; }