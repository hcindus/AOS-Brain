package com.psdepot.appointments.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
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
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardCapitalization
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.psdepot.appointments.data.model.AppointmentStatus
import com.psdepot.appointments.data.model.LeadInfo
import com.psdepot.appointments.ui.theme.PSDBlue
import com.psdepot.appointments.ui.theme.PSDOrange
import com.psdepot.appointments.ui.viewmodel.BookingViewModel
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.LocalTime
import java.time.format.DateTimeFormatter

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BookingScreen(
    onBack: () -> Unit,
    onBookingComplete: () -> Unit,
    viewModel: BookingViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    var showServiceTypeMenu by remember { mutableStateOf(false) }
    var showTimePicker by remember { mutableStateOf(false) }
    var showDatePicker by remember { mutableStateOf(false) }
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("New Booking") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    TextButton(
                        onClick = { viewModel.submitBooking() },
                        enabled = uiState.canSubmit && !uiState.isLoading
                    ) {
                        Text("Save")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Error message
            uiState.error?.let { error ->
                Surface(
                    color = MaterialTheme.colorScheme.errorContainer,
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Row(
                        modifier = Modifier.padding(12.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            Icons.Default.Error,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.error
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(
                            text = error,
                            color = MaterialTheme.colorScheme.error
                        )
                    }
                }
            }
            
            // Selected Lead (if any)
            uiState.selectedLead?.let { lead ->
                Surface(
                    color = PSDBlue.copy(alpha = 0.1f),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(12.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            Icons.Default.Person,
                            contentDescription = null,
                            tint = PSDBlue
                        )
                        Spacer(modifier = Modifier.width(12.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                text = lead.contactName ?: lead.companyName ?: "Unknown",
                                style = MaterialTheme.typography.bodyLarge
                            )
                            Text(
                                text = "${lead.email ?: ""} ${lead.phone ?: ""}",
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                        IconButton(onClick = { viewModel.clearSelectedLead() }) {
                            Icon(Icons.Default.Clear, contentDescription = "Remove")
                        }
                    }
                }
            }
            
            // Customer Information
            Text(
                text = "Customer Information",
                style = MaterialTheme.typography.titleMedium
            )
            
            OutlinedTextField(
                value = uiState.customerName,
                onValueChange = viewModel::onCustomerNameChange,
                label = { Text("Customer Name *") },
                leadingIcon = { Icon(Icons.Default.Person, null) },
                singleLine = true,
                modifier = Modifier.fillMaxWidth()
            )
            
            OutlinedTextField(
                value = uiState.customerEmail,
                onValueChange = viewModel::onCustomerEmailChange,
                label = { Text("Email") },
                leadingIcon = { Icon(Icons.Default.Email, null) },
                singleLine = true,
                modifier = Modifier.fillMaxWidth()
            )
            
            OutlinedTextField(
                value = uiState.customerPhone,
                onValueChange = viewModel::onCustomerPhoneChange,
                label = { Text("Phone") },
                leadingIcon = { Icon(Icons.Default.Phone, null) },
                singleLine = true,
                modifier = Modifier.fillMaxWidth()
            )
            
            Divider(modifier = Modifier.padding(vertical = 8.dp))
            
            // Appointment Details
            Text(
                text = "Appointment Details",
                style = MaterialTheme.typography.titleMedium
            )
            
            // Service Type Dropdown
            ExposedDropdownMenuBox(
                expanded = showServiceTypeMenu,
                onExpandedChange = { showServiceTypeMenu = it }
            ) {
                OutlinedTextField(
                    value = uiState.serviceType.replaceFirstChar { it.uppercase() },
                    onValueChange = {},
                    readOnly = true,
                    label = { Text("Service Type") },
                    trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = showServiceTypeMenu) },
                    modifier = Modifier
                        .fillMaxWidth()
                        .menuAnchor()
                )
                
                ExposedDropdownMenu(
                    expanded = showServiceTypeMenu,
                    onDismissRequest = { showServiceTypeMenu = false }
                ) {
                    val serviceTypes = listOf("consultation", "installation", "support", "training", "demo")
                    serviceTypes.forEach { type ->
                        DropdownMenuItem(
                            text = { Text(type.replaceFirstChar { it.uppercase() }) },
                            onClick = {
                                viewModel.onServiceTypeChange(type)
                                showServiceTypeMenu = false
                            }
                        )
                    }
                }
            }
            
            // Date Selection
            OutlinedCard(
                modifier = Modifier.fillMaxWidth(),
                onClick = { showDatePicker = true }
            ) {
                Row(
                    modifier = Modifier.padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(Icons.Default.CalendarToday, contentDescription = null)
                    Spacer(modifier = Modifier.width(16.dp))
                    Column {
                        Text(
                            text = "Date",
                            style = MaterialTheme.typography.bodySmall
                        )
                        Text(
                            text = uiState.selectedDate.format(DateTimeFormatter.ofPattern("EEEE, MMMM d, yyyy")),
                            style = MaterialTheme.typography.bodyLarge
                        )
                    }
                }
            }
            
            // Time Selection
            OutlinedCard(
                modifier = Modifier.fillMaxWidth(),
                onClick = { showTimePicker = true }
            ) {
                Row(
                    modifier = Modifier.padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(Icons.Default.Schedule, contentDescription = null)
                    Spacer(modifier = Modifier.width(16.dp))
                    Column {
                        Text(
                            text = "Time",
                            style = MaterialTheme.typography.bodySmall
                        )
                        Text(
                            text = uiState.selectedTime.format(DateTimeFormatter.ofPattern("h:mm a")),
                            style = MaterialTheme.typography.bodyLarge
                        )
                    }
                }
            }
            
            // Duration
            Row(
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("Duration: ${uiState.durationMinutes} minutes")
                Spacer(modifier = Modifier.width(16.dp))
                Slider(
                    value = uiState.durationMinutes.toFloat(),
                    onValueChange = { viewModel.onDurationChange(it.toInt()) },
                    valueRange = 15f..180f,
                    steps = 10,
                    modifier = Modifier.weight(1f)
                )
            }
            
            // Notes
            OutlinedTextField(
                value = uiState.notes,
                onValueChange = viewModel::onNotesChange,
                label = { Text("Notes") },
                minLines = 3,
                maxLines = 5,
                modifier = Modifier.fillMaxWidth()
            )
            
            Spacer(modifier = Modifier.height(32.dp))
            
            // Submit Button
            Button(
                onClick = { viewModel.submitBooking() },
                enabled = uiState.canSubmit && !uiState.isLoading,
                modifier = Modifier.fillMaxWidth()
            ) {
                if (uiState.isLoading) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(20.dp),
                        color = MaterialTheme.colorScheme.onPrimary
                    )
                } else {
                    Icon(Icons.Default.Check, contentDescription = null)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Create Booking")
                }
            }
        }
    }
    
    // Success dialog
    if (uiState.isSuccess) {
        AlertDialog(
            onDismissRequest = onBookingComplete,
            icon = { Icon(Icons.Default.CheckCircle, contentDescription = null) },
            title = { Text("Booking Confirmed") },
            text = { Text("The appointment has been scheduled successfully.") },
            confirmButton = {
                TextButton(onClick = onBookingComplete) {
                    Text("Done")
                }
            }
        )
    }
    
    // Date Picker Dialog
    if (showDatePicker) {
        val datePickerState = rememberDatePickerState(
            initialSelectedDateMillis = uiState.selectedDate
                .atStartOfDay(java.time.ZoneId.systemDefault())
                .toInstant()
                .toEpochMilli()
        )
        
        DatePickerDialog(
            onDismissRequest = { showDatePicker = false },
            confirmButton = {
                TextButton(
                    onClick = {
                        datePickerState.selectedDateMillis?.let { millis ->
                            val date = java.time.Instant.ofEpochMilli(millis)
                                .atZone(java.time.ZoneId.systemDefault())
                                .toLocalDate()
                            viewModel.onDateChange(date)
                        }
                        showDatePicker = false
                    }
                ) {
                    Text("OK")
                }
            },
            dismissButton = {
                TextButton(onClick = { showDatePicker = false }) {
                    Text("Cancel")
                }
            }
        ) {
            DatePicker(state = datePickerState)
        }
    }
    
    // Time Picker Dialog
    if (showTimePicker) {
        val timePickerState = rememberTimePickerState(
            initialHour = uiState.selectedTime.hour,
            initialMinute = uiState.selectedTime.minute
        )
        
        AlertDialog(
            onDismissRequest = { showTimePicker = false },
            title = { Text("Select Time") },
            text = {
                TimePicker(state = timePickerState)
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        viewModel.onTimeChange(
                            LocalTime.of(timePickerState.hour, timePickerState.minute)
                        )
                        showTimePicker = false
                    }
                ) {
                    Text("OK")
                }
            },
            dismissButton = {
                TextButton(onClick = { showTimePicker = false }) {
                    Text("Cancel")
                }
            }
        )
    }
}
