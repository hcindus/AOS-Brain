package com.psdepot.appointments

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.psdepot.appointments.ui.screens.LoginScreen
import com.psdepot.appointments.ui.screens.adaptive.AdaptiveCalendarScreen
import com.psdepot.appointments.ui.screens.AppointmentsListScreen
import com.psdepot.appointments.ui.screens.BookingScreen
import com.psdepot.appointments.ui.screens.AppointmentDetailScreen
import com.psdepot.appointments.ui.screens.LeadsSearchScreen
import com.psdepot.appointments.ui.theme.PSDAppointmentsTheme
import com.psdepot.appointments.ui.viewmodel.AuthViewModel
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            PSDAppointmentsTheme(darkTheme = true) {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    AppointmentsApp()
                }
            }
        }
    }
}

@Composable
fun AppointmentsApp(
    authViewModel: AuthViewModel = hiltViewModel()
) {
    val navController = rememberNavController()
    val authState by authViewModel.authState.collectAsState()
    
    LaunchedEffect(authState) {
        when (authState) {
            is AuthViewModel.AuthState.Authenticated -> {
                navController.navigate("calendar") {
                    popUpTo(0) { inclusive = true }
                }
            }
            is AuthViewModel.AuthState.Unauthenticated -> {
                navController.navigate("login") {
                    popUpTo(0) { inclusive = true }
                }
            }
            else -> { /* Loading state */ }
        }
    }
    
    NavHost(
        navController = navController,
        startDestination = "loading"
    ) {
        composable("loading") {
            // Splash/Loading screen
            LaunchedEffect(Unit) {
                authViewModel.checkAuthStatus()
            }
        }
        
        composable("login") {
            LoginScreen(
                onLoginSuccess = {
                    navController.navigate("calendar") {
                        popUpTo("login") { inclusive = true }
                    }
                }
            )
        }
        
        composable("calendar") {
            AdaptiveCalendarScreen(
                onNewBooking = {
                    navController.navigate("booking")
                },
                onAppointmentClick = { appointmentId ->
                    navController.navigate("appointment/$appointmentId")
                },
                onSearchLeads = {
                    navController.navigate("leads")
                },
                onNavigate = { route ->
                    when (route) {
                        "calendar" -> { /* Already on calendar */ }
                        "appointments" -> navController.navigate("appointments_list")
                        "leads" -> navController.navigate("leads")
                        "settings" -> navController.navigate("settings")
                    }
                },
                currentRoute = "calendar"
            )
        }
        
        composable("appointments_list") {
            AppointmentsListScreen(
                onBack = { navController.navigateUp() },
                onAppointmentClick = { appointmentId ->
                    navController.navigate("appointment/$appointmentId")
                }
            )
        }
        
        composable("booking") {
            BookingScreen(
                onBack = { navController.navigateUp() },
                onBookingComplete = {
                    navController.navigateUp()
                }
            )
        }
        
        composable("appointment/{appointmentId}") { backStackEntry ->
            val appointmentId = backStackEntry.arguments?.getString("appointmentId") ?: ""
            AppointmentDetailScreen(
                appointmentId = appointmentId,
                onBack = { navController.navigateUp() },
                onEdit = { /* TODO */ }
            )
        }
        
        composable("leads") {
            LeadsSearchScreen(
                onBack = { navController.navigateUp() },
                onLeadSelected = { lead ->
                    navController.previousBackStackEntry
                        ?.savedStateHandle
                        ?.set("selected_lead", lead)
                    navController.navigateUp()
                }
            )
        }
    }
}
