package com.ps.pos

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.ps.pos.ui.screens.ProductManagementScreen
import com.ps.pos.ui.screens.RegisterScreen
import com.ps.pos.ui.screens.SettingsScreen
import com.ps.pos.ui.screens.TransactionHistoryScreen
import com.ps.pos.ui.theme.RS80Theme
import com.ps.pos.viewmodel.RegisterViewModel

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            RS80Theme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    POSApp()
                }
            }
        }
    }
}

@Composable
fun POSApp() {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = "register") {
        composable("register") {
            RegisterScreen(
                viewModel = viewModel(),
                onNavigateToProducts = { navController.navigate("products") },
                onNavigateToTransactions = { navController.navigate("transactions") },
                onNavigateToSettings = { navController.navigate("settings") }
            )
        }
        composable("products") {
            ProductManagementScreen(
                onBack = { navController.popBackStack() }
            )
        }
        composable("transactions") {
            TransactionHistoryScreen(
                onBack = { navController.popBackStack() }
            )
        }
        composable("settings") {
            SettingsScreen(
                onBack = { navController.popBackStack() }
            )
        }
    }
}