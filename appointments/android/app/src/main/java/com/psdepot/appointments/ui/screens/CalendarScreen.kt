package com.psdepot.appointments.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.ArrowForward
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.psdepot.appointments.data.model.Appointment
import com.psdepot.appointments.data.model.AvailabilitySlot
import com.psdepot.appointments.ui.theme.PSDBlue
import com.psdepot.appointments.ui.theme.PSDOrange
import com.psdepot.appointments.ui.viewmodel.CalendarViewModel
import java.time.LocalDate
import java.time.LocalTime
import java.time.format.DateTimeFormatter

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CalendarScreen(
    onNewBooking: () -> Unit,
    onAppointmentClick: (String) -> Unit,
    onSearchLeads: () -> Unit,
    viewModel: CalendarViewModel = hiltViewModel()
) {
    val selectedDate by viewModel.selectedDate.collectAsState()
    val availabilitySlots by viewModel.availabilitySlots.collectAsState()
    val appointments by viewModel.appointments.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    
    val weekDays = remember(selectedDate) {
        val startOfWeek = selectedDate.minusDays(selectedDate.dayOfWeek.value.toLong() - 1)
        (0..6).map { startOfWeek.plusDays(it.toLong()) }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { 
                    Text(
                        selectedDate.format(DateTimeFormatter.ofPattern("MMMM yyyy")),
                        style = MaterialTheme.typography.titleLarge
                    )
                },
                actions = {
                    IconButton(onClick = onSearchLeads) {
                        Icon(Icons.Default.Search, contentDescription = "Search leads")
                    }
                }
            )
        },
        floatingActionButton = {
            FloatingActionButton(
                onClick = onNewBooking,
                containerColor = PSDOrange
            ) {
                Icon(Icons.Default.Add, contentDescription = "New booking")
            }
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            // Week Navigation
            WeekNavigationBar(
                weekDays = weekDays,
                selectedDate = selectedDate,
                onDateSelected = { viewModel.selectDate(it) },
                onPreviousWeek = { viewModel.previousWeek() },
                onNextWeek = { viewModel.nextWeek() }
            )
            
            // Time Slots
            if (isLoading) {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator()
                }
            } else {
                LazyColumn(
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(availabilitySlots) { slot ->
                        TimeSlotCard(
                            slot = slot,
                            appointment = appointments.find { 
                                it.scheduledAt.contains(slot.slotTime.toString()) 
                            },
                            onClick = { 
                                slot.appointmentId?.let(onAppointmentClick) ?: onNewBooking()
                            }
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun WeekNavigationBar(
    weekDays: List<LocalDate>,
    selectedDate: LocalDate,
    onDateSelected: (LocalDate) -> Unit,
    onPreviousWeek: () -> Unit,
    onNextWeek: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        IconButton(onClick = onPreviousWeek) {
            Icon(Icons.Default.ArrowBack, contentDescription = "Previous week")
        }
        
        Row(
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            weekDays.forEach { date ->
                val isSelected = date == selectedDate
                val isToday = date == LocalDate.now()
                
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier
                        .clip(RoundedCornerShape(8.dp))
                        .background(
                            when {
                                isSelected -> PSDBlue
                                isToday -> PSDOrange.copy(alpha = 0.2f)
                                else -> Color.Transparent
                            }
                        )
                        .clickable { onDateSelected(date) }
                        .padding(horizontal = 12.dp, vertical = 8.dp)
                ) {
                    Text(
                        text = date.dayOfWeek.name.take(3),
                        style = MaterialTheme.typography.bodySmall,
                        color = if (isSelected) Color.White else MaterialTheme.colorScheme.onSurface
                    )
                    Text(
                        text = date.dayOfMonth.toString(),
                        style = MaterialTheme.typography.titleMedium,
                        color = if (isSelected) Color.White else MaterialTheme.colorScheme.onSurface
                    )
                }
            }
        }
        
        IconButton(onClick = onNextWeek) {
            Icon(Icons.Default.ArrowForward, contentDescription = "Next week")
        }
    }
}

@Composable
fun TimeSlotCard(
    slot: AvailabilitySlot,
    appointment: Appointment?,
    onClick: () -> Unit
) {
    val backgroundColor = when {
        appointment != null -> PSDOrange.copy(alpha = 0.1f)
        slot.isAvailable -> MaterialTheme.colorScheme.surface
        else -> MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
    }
    
    val borderColor = when {
        appointment != null -> PSDOrange
        slot.isAvailable -> MaterialTheme.colorScheme.outline.copy(alpha = 0.3f)
        else -> Color.Transparent
    }
    
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        colors = CardDefaults.cardColors(containerColor = backgroundColor),
        border = androidx.compose.foundation.BorderStroke(1.dp, borderColor)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Time
            Text(
                text = slot.slotTime.format(DateTimeFormatter.ofPattern("h:mm a")),
                style = MaterialTheme.typography.titleMedium,
                modifier = Modifier.width(80.dp)
            )
            
            // Status / Appointment Info
            when {
                appointment != null -> {
                    Column {
                        Text(
                            text = appointment.customerName,
                            style = MaterialTheme.typography.bodyLarge
                        )
                        Text(
                            text = appointment.serviceType,
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
                slot.isAvailable -> {
                    Text(
                        text = "Available",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.primary
                    )
                }
                else -> {
                    Text(
                        text = "Blocked",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
    }
}
