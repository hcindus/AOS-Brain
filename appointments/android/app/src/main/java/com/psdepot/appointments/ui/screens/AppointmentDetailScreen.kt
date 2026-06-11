package com.psdepot.appointments.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.psdepot.appointments.data.model.Appointment
import com.psdepot.appointments.data.model.AppointmentStatus
import com.psdepot.appointments.ui.theme.PSDBlue
import com.psdepot.appointments.ui.theme.PSDOrange
import com.psdepot.appointments.ui.viewmodel.AppointmentDetailViewModel
import java.time.format.DateTimeFormatter

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AppointmentDetailScreen(
    appointmentId: String,
    onBack: () -> Unit,
    onEdit: () -> Unit,
    viewModel: AppointmentDetailViewModel = hiltViewModel()
) {
    val appointment by viewModel.appointment.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    val showCancelDialog by viewModel.showCancelDialog.collectAsState()

    LaunchedEffect(appointmentId) {
        viewModel.loadAppointment(appointmentId)
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Appointment Details") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    appointment?.let { appt ->
                        if (appt.status != AppointmentStatus.CANCELLED && 
                            appt.status != AppointmentStatus.COMPLETED) {
                            IconButton(onClick = onEdit) {
                                Icon(Icons.Default.Edit, contentDescription = "Edit")
                            }
                        }
                    }
                }
            )
        }
    ) { padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            when {
                isLoading -> {
                    CircularProgressIndicator(
                        modifier = Modifier.align(Alignment.Center),
                        color = PSDOrange
                    )
                }
                appointment == null -> {
                    Text(
                        text = "Appointment not found",
                        modifier = Modifier.align(Alignment.Center)
                    )
                }
                else -> {
                    AppointmentDetailContent(
                        appointment = appointment!!,
                        onMarkComplete = { viewModel.markComplete() },
                        onCancel = { viewModel.showCancelDialog() }
                    )
                }
            }
        }
    }

    // Cancel Confirmation Dialog
    if (showCancelDialog) {
        AlertDialog(
            onDismissRequest = { viewModel.dismissCancelDialog() },
            title = { Text("Cancel Appointment") },
            text = { Text("Are you sure you want to cancel this appointment?") },
            confirmButton = {
                TextButton(
                    onClick = { viewModel.cancelAppointment() },
                    colors = ButtonDefaults.textButtonColors(
                        contentColor = MaterialTheme.colorScheme.error
                    )
                ) {
                    Text("Cancel Appointment")
                }
            },
            dismissButton = {
                TextButton(onClick = { viewModel.dismissCancelDialog() }) {
                    Text("Keep")
                }
            }
        )
    }
}

@Composable
private fun AppointmentDetailContent(
    appointment: Appointment,
    onMarkComplete: () -> Unit,
    onCancel: () -> Unit
) {
    val statusColor = when (appointment.status) {
        AppointmentStatus.CONFIRMED -> Color(0xFF4CAF50)
        AppointmentStatus.COMPLETED -> PSDBlue
        AppointmentStatus.CANCELLED -> Color(0xFFF44336)
        AppointmentStatus.NO_SHOW -> Color(0xFFFF9800)
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // Status Card
        Card(
            modifier = Modifier.fillMaxWidth(),
            colors = CardDefaults.cardColors(
                containerColor = statusColor.copy(alpha = 0.1f)
            )
        ) {
            Row(
                modifier = Modifier.padding(16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Surface(
                    color = statusColor,
                    shape = RoundedCornerShape(4.dp),
                    modifier = Modifier.size(12.dp)
                ) {}
                
                Spacer(modifier = Modifier.width(12.dp))
                
                Text(
                    text = appointment.status.name.lowercase().replaceFirstChar { it.uppercase() },
                    style = MaterialTheme.typography.titleMedium,
                    color = statusColor
                )
            }
        }

        // Customer Info Card
        Card(
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(
                modifier = Modifier.padding(16.dp)
            ) {
                Text(
                    text = "Customer",
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                
                Spacer(modifier = Modifier.height(8.dp))
                
                Text(
                    text = appointment.customerName,
                    style = MaterialTheme.typography.headlineSmall
                )
                
                if (!appointment.customerEmail.isNullOrBlank()) {
                    Spacer(modifier = Modifier.height(8.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(
                            Icons.Default.Email,
                            contentDescription = null,
                            modifier = Modifier.size(18.dp)
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(
                            text = appointment.customerEmail,
                            style = MaterialTheme.typography.bodyMedium
                        )
                    }
                }
                
                if (!appointment.customerPhone.isNullOrBlank()) {
                    Spacer(modifier = Modifier.height(8.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(
                            Icons.Default.Phone,
                            contentDescription = null,
                            modifier = Modifier.size(18.dp)
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(
                            text = appointment.customerPhone,
                            style = MaterialTheme.typography.bodyMedium
                        )
                    }
                }
            }
        }

        // Appointment Details Card
        Card(
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(
                modifier = Modifier.padding(16.dp)
            ) {
                Text(
                    text = "Details",
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                
                Spacer(modifier = Modifier.height(12.dp))
                
                // Date & Time
                DetailRow(
                    icon = Icons.Default.CalendarToday,
                    label = "Date",
                    value = appointment.scheduledAt.format(
                        DateTimeFormatter.ofPattern("EEEE, MMMM d, yyyy")
                    )
                )
                
                Spacer(modifier = Modifier.height(8.dp))
                
                DetailRow(
                    icon = Icons.Default.Schedule,
                    label = "Time",
                    value = appointment.scheduledAt.format(
                        DateTimeFormatter.ofPattern("h:mm a")
                    ) + " (${appointment.durationMinutes} min)"
                )
                
                Spacer(modifier = Modifier.height(8.dp))
                
                DetailRow(
                    icon = Icons.Default.Business,
                    label = "Service",
                    value = appointment.serviceType.replaceFirstChar { it.uppercase() }
                )
                
                if (!appointment.googleEventId.isNullOrBlank()) {
                    Spacer(modifier = Modifier.height(8.dp))
                    DetailRow(
                        icon = Icons.Default.CloudSync,
                        label = "Calendar",
                        value = "Synced to Google Calendar"
                    )
                }
            }
        }

        // Notes Card
        if (!appointment.notes.isNullOrBlank()) {
            Card(
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(
                    modifier = Modifier.padding(16.dp)
                ) {
                    Text(
                        text = "Notes",
                        style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    Text(
                        text = appointment.notes,
                        style = MaterialTheme.typography.bodyMedium
                    )
                }
            }
        }

        // Actions
        if (appointment.status == AppointmentStatus.CONFIRMED) {
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                Button(
                    onClick = onMarkComplete,
                    modifier = Modifier.weight(1f)
                ) {
                    Icon(Icons.Default.CheckCircle, contentDescription = null)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Mark Complete")
                }
                
                OutlinedButton(
                    onClick = onCancel,
                    modifier = Modifier.weight(1f),
                    colors = ButtonDefaults.outlinedButtonColors(
                        contentColor = MaterialTheme.colorScheme.error
                    )
                ) {
                    Icon(Icons.Default.Cancel, contentDescription = null)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Cancel")
                }
            }
        }

        Spacer(modifier = Modifier.height(32.dp))
    }
}

@Composable
private fun DetailRow(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    label: String,
    value: String
) {
    Row(
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            modifier = Modifier.size(20.dp),
            tint = MaterialTheme.colorScheme.onSurfaceVariant
        )
        
        Spacer(modifier = Modifier.width(12.dp))
        
        Column {
            Text(
                text = label,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            Text(
                text = value,
                style = MaterialTheme.typography.bodyLarge
            )
        }
    }
}
