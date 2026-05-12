package com.psdepot.appointments.ui.screens.adaptive

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.unit.dp
import androidx.window.core.layout.WindowSizeClass
import androidx.window.core.layout.WindowWidthSizeClass
import com.psdepot.appointments.ui.screens.mobile.MobileCalendarContent
import com.psdepot.appointments.ui.screens.desktop.DesktopCalendarContent
import com.psdepot.appointments.ui.theme.PSDBlue
import com.psdepot.appointments.ui.theme.PSDOrange

/**
 * Adaptive Calendar Screen
 * Switches between mobile (bottom nav) and desktop (side rail) layouts
 */
@Composable
fun AdaptiveCalendarScreen(
    onNewBooking: () -> Unit,
    onAppointmentClick: (String) -> Unit,
    onSearchLeads: () -> Unit,
    onNavigate: (String) -> Unit,
    currentRoute: String
) {
    val windowSizeClass = calculateWindowSizeClass()
    val isCompact = windowSizeClass.widthSizeClass == WindowWidthSizeClass.COMPACT
    
    // Track selected nav item
    var selectedNavItem by remember { mutableStateOf(0) }
    
    val navItems = listOf(
        NavItem("calendar", Icons.Default.CalendarToday, "Calendar"),
        NavItem("appointments", Icons.Default.List, "Appointments"),
        NavItem("leads", Icons.Default.Search, "Leads"),
        NavItem("settings", Icons.Default.Settings, "Settings")
    )
    
    Scaffold(
        topBar = {
            if (!isCompact) {
                // Desktop: Top app bar with title
                TopAppBar(
                    title = { Text("PSD Appointments") },
                    colors = TopAppBarDefaults.topAppBarColors(
                        containerColor = PSDBlue,
                        titleContentColor = MaterialTheme.colorScheme.onPrimary
                    )
                )
            }
        },
        bottomBar = {
            if (isCompact) {
                // Mobile: Bottom navigation
                NavigationBar(
                    containerColor = MaterialTheme.colorScheme.surface
                ) {
                    navItems.forEachIndexed { index, item ->
                        NavigationBarItem(
                            icon = { Icon(item.icon, contentDescription = item.label) },
                            label = { Text(item.label) },
                            selected = selectedNavItem == index,
                            onClick = {
                                selectedNavItem = index
                                onNavigate(item.route)
                            },
                            colors = NavigationBarItemDefaults.colors(
                                selectedIconColor = PSDOrange,
                                selectedTextColor = PSDOrange
                            )
                        )
                    }
                }
            }
        },
        floatingActionButton = {
            ExtendedFloatingActionButton(
                onClick = onNewBooking,
                icon = { Icon(Icons.Default.Add, "New booking") },
                text = { Text("Book") },
                containerColor = PSDOrange
            )
        }
    ) { padding ->
        if (isCompact) {
            // Mobile Layout
            MobileCalendarContent(
                onAppointmentClick = onAppointmentClick,
                onSearchLeads = onSearchLeads,
                modifier = Modifier.padding(padding)
            )
        } else {
            // Desktop/Tablet Layout with side navigation
            Row(modifier = Modifier.padding(padding)) {
                // Side Navigation Rail
                NavigationRail(
                    containerColor = MaterialTheme.colorScheme.surfaceVariant
                ) {
                    navItems.forEachIndexed { index, item ->
                        NavigationRailItem(
                            icon = { Icon(item.icon, contentDescription = item.label) },
                            label = { Text(item.label) },
                            selected = selectedNavItem == index,
                            onClick = {
                                selectedNavItem = index
                                onNavigate(item.route)
                            },
                            colors = NavigationRailItemDefaults.colors(
                                selectedIconColor = PSDOrange,
                                selectedTextColor = PSDOrange
                            )
                        )
                    }
                }
                
                // Main Content
                DesktopCalendarContent(
                    onAppointmentClick = onAppointmentClick,
                    onSearchLeads = onSearchLeads,
                    modifier = Modifier.weight(1f)
                )
            }
        }
    }
}

data class NavItem(
    val route: String,
    val icon: androidx.compose.ui.graphics.vector.ImageVector,
    val label: String
)

@Composable
fun calculateWindowSizeClass(): WindowSizeClass {
    val configuration = LocalConfiguration.current
    val widthDp = configuration.screenWidthDp
    
    return WindowSizeClass.compute(widthDp, configuration.screenHeightDp)
}

// Extension to get width size class
val WindowSizeClass.widthSizeClass: WindowWidthSizeClass
    get() = when {
        this.windowWidthDp < 600 -> WindowWidthSizeClass.COMPACT
        this.windowWidthDp < 840 -> WindowWidthSizeClass.MEDIUM
        else -> WindowWidthSizeClass.EXPANDED
    }

// Window size class enum for compatibility
object WindowWidthSizeClass {
    const val COMPACT = 0
    const val MEDIUM = 1
    const val EXPANDED = 2
}
