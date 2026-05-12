package com.psdepot.appointments.ui.screens.desktop

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
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
import com.psdepot.appointments.data.model.AppointmentStatus
import com.psdepot.appointments.data.model.AvailabilitySlot
import com.psdepot.appointments.ui.theme.PSDBlue
import com.psdepot.appointments.ui.theme.PSDOrange
import com.psdepot.appointments.ui.viewmodel.CalendarViewModel
import java.time.LocalDate
import java.time.format.DateTimeFormatter

/**
 * Desktop/Tablet-optimized calendar view
 * Features: Side-by-side layout, weekly grid, appointment details panel
 */
@Composable
fun DesktopCalendarContent(
    onAppointmentClick: (String) -> Unit,
    onSearchLeads: () -> Unit,
    modifier: Modifier = Modifier,
    viewModel: CalendarViewModel = hiltViewModel()
) {
    val selectedDate by viewModel.selectedDate.collectAsState()
    val availabilitySlots by viewModel.availabilitySlots.collectAsState()
    val appointments by viewModel.appointments.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    
    var selectedAppointment by remember { mutableStateOf<Appointment?>(null) }
    
    val weekDays = remember(selectedDate) {
        val startOfWeek = selectedDate.minusDays(selectedDate.dayOfWeek.value.toLong() - 1)
        (0..6).map { startOfWeek.plusDays(it.toLong()) }
    }

    Row(modifier = modifier.fillMaxSize()) {
        // Left Panel: Calendar
        Column(
            modifier = Modifier
                .weight(2f)
                .fillMaxHeight()
                .padding(16.dp)
        ) {
            // Week grid header
            DesktopWeekHeader(
                weekDays = weekDays,
                selectedDate = selectedDate,
                onDateSelected = { viewModel.selectDate(it) },
                onPreviousWeek = { viewModel.previousWeek() },
                onNextWeek = { viewModel.nextWeek() }
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // Week grid or time slots
            if (isLoading) {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator(color = PSDOrange)
                }
            } else {
                // Desktop: Show weekly grid view
                DesktopWeekGrid(
                    weekDays = weekDays,
                    availabilitySlots = availabilitySlots,
                    appointments = appointments,
                    onSlotClick = { slot, appt ->
                        appt?.let { 
                            selectedAppointment = it
                            onAppointmentClick(it.id)
                        } ?: onSearchLeads()
                    }
                )
            }
        }
        
        // Right Panel: Details / Quick Actions
        DesktopSidePanel(
            selectedDate = selectedDate,
            appointments = appointments,
            selectedAppointment = selectedAppointment,
            onAppointmentSelect = { selectedAppointment = it },
            onSearchLeads = onSearchLeads,
            modifier = Modifier
                .weight(1f)
                .fillMaxHeight()
                .padding(end = 16.dp, top = 16.dp, bottom = 16.dp)
        )
    }
}

@Composable
fun DesktopWeekHeader(
    weekDays: List<LocalDate>,
    selectedDate: LocalDate,
    onDateSelected: (LocalDate) -> Unit,
    onPreviousWeek: () -> Unit,
    onNextWeek: () -> Unit
) {
    Surface(
        tonalElevation = 1.dp,
        shape = RoundedCornerShape(12.dp),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            // Month navigation
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(onClick = onPreviousWeek) {
                    Icon(Icons.Default.ChevronLeft, "Previous week")
                }
                
                Text(
                    text = selectedDate.format(DateTimeFormatter.ofPattern("MMMM yyyy")),
                    style = MaterialTheme.typography.headlineSmall
                )
                
                IconButton(onClick = onNextWeek) {
                    Icon(Icons.Default.ChevronRight, "Next week")
                }
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // Day columns
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
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
                            .padding(horizontal = 24.dp, vertical = 12.dp)
                    ) {
                        Text(
                            text = date.dayOfWeek.name.take(3),
                            style = MaterialTheme.typography.bodyMedium,
                            color = when {
                                isSelected -> Color.White
                                else -> MaterialTheme.colorScheme.onSurface
                            }
                        )
                        Text(
                            text = date.dayOfMonth.toString(),
                            style = MaterialTheme.typography.headlineSmall,
                            color = when {
                                isSelected -> Color.White
                                else -> MaterialTheme.colorScheme.onSurface
                            }
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun DesktopWeekGrid(
    weekDays: List<LocalDate>,
    availabilitySlots: List<AvailabilitySlot>,
    appointments: List<Appointment>,
    onSlotClick: (AvailabilitySlot, Appointment?) -> Unit
) {
    // Group slots by day
    val slotsByDay = availabilitySlots.groupBy { it.slotDate }
    
    Surface(
        tonalElevation = 1.dp,
        shape = RoundedCornerShape(12.dp)
    ) {
        Row(modifier = Modifier.fillMaxSize()) {
            weekDays.forEach { date ->
                val daySlots = slotsByDay[date] ?: emptyList()
                val dayAppointments = appointments.filter { 
                    it.scheduledAt.toLocalDate() == date 
                }
                
                Column(
                    modifier = Modifier
                        .weight(1f)
                        .padding(8.dp)
                ) {
                    // Day header
                    Text(
                        text = date.format(DateTimeFormatter.ofPattern("EEE")),
                        style = MaterialTheme.typography.labelMedium,
                        modifier = Modifier.fillMaxWidth(),
                        textAlign = TextAlign.Center
                    )
                    
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    // Time slots for this day
                    LazyColumn(
                        verticalArrangement = Arrangement.spacedBy(4.dp),
                        modifier = Modifier.fillMaxHeight()
                    ) {
                        items(daySlots.take(8)) { slot ->
                            val appointment = dayAppointments.find { 
                                it.scheduledAt.toLocalTime() == slot.slotTime 
                            }
                            
                            DesktopGridSlot(
                                slot = slot,
                                appointment = appointment,
                                onClick = { onSlotClick(slot, appointment) }
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun DesktopGridSlot(
    slot: AvailabilitySlot,
    appointment: Appointment?,
    onClick: () -> Unit
) {
    val backgroundColor = when {
        appointment != null -> PSDOrange.copy(alpha = 0.15f)
        slot.isAvailable -> MaterialTheme.colorScheme.surface
        else -> MaterialTheme.colorScheme.surfaceVariant
    }
    
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .height(60.dp)
            .clickable(onClick = onClick),
        color = backgroundColor,
        shape = RoundedCornerShape(6.dp),
        tonalElevation = if (appointment != null) 2.dp else 0.dp
    ) {
        Column(
            modifier = Modifier.padding(8.dp),
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            Text(
                text = slot.slotTime.format(DateTimeFormatter.ofPattern("h:mm a")),
                style = MaterialTheme.typography.labelSmall
            )
            
            appointment?.let {
                Text(
                    text = it.customerName,
                    style = MaterialTheme.typography.bodySmall,
                    maxLines = 1
                )
            }
        }
    }
}

@Composable
fun DesktopSidePanel(
    selectedDate: LocalDate,
    appointments: List<Appointment>,
    selectedAppointment: Appointment?,
    onAppointmentSelect: (Appointment) -> Unit,
    onSearchLeads: () -> Unit,
    modifier: Modifier = Modifier
) {
    Surface(
        tonalElevation = 2.dp,
        shape = RoundedCornerShape(12.dp),
        modifier = modifier.widthIn(min = 280.dp, max = 360.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            // Header
            Text(
                text = "Today's Schedule",
                style = MaterialTheme.typography.titleMedium
            )
            
            Text(
                text = selectedDate.format(DateTimeFormatter.ofPattern("EEEE, MMMM d")),
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Divider()
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // Appointments list
            if (appointments.isEmpty()) {
                Box(
                    modifier = Modifier.fillMaxWidth().weight(1f),
                    contentAlignment = Alignment.Center
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(
                            Icons.Default.EventAvailable,
                            contentDescription = null,
                            modifier = Modifier.size(48.dp),
                            tint = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = "No appointments",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            } else {
                LazyColumn(
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                    modifier = Modifier.weight(1f)
                ) {
                    items(appointments) { appointment ->
                        DesktopAppointmentCard(
                            appointment = appointment,
                            isSelected = appointment.id == selectedAppointment?.id,
                            onClick = { onAppointmentSelect(appointment) }
                        )
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // Quick Actions
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(
                    onClick = onSearchLeads,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Icon(Icons.Default.Add, contentDescription = null)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("New Booking")
                }
                
                OutlinedButton(
                    onClick = { /* Export calendar */ },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Icon(Icons.Default.Share, contentDescription = null)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Export")
                }
            }
        }
    }
}

@Composable
fun DesktopAppointmentCard(
    appointment: Appointment,
    isSelected: Boolean,
    onClick: () -> Unit
) {
    Surface(
        modifier = Modifier.fillMaxWidth().clickable(onClick = onClick),
        color = when {
            isSelected -> PSDOrange.copy(alpha = 0.1f)
            else -> MaterialTheme.colorScheme.surface
        },
        shape = RoundedCornerShape(8.dp),
        tonalElevation = if (isSelected) 2.dp else 0.dp
    ) {
        Row(
            modifier = Modifier.padding(12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Time
            Column(horizontalAlignment = Alignment.End, modifier = Modifier.width(60.dp)) {
                Text(
                    text = appointment.scheduledAt.format(DateTimeFormatter.ofPattern("h:mm")),
                    style = MaterialTheme.typography.bodyMedium
                )
                Text(
                    text = appointment.scheduledAt.format(DateTimeFormatter.ofPattern("a")),
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            
            Spacer(modifier = Modifier.width(12.dp))
            
            // Info
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = appointment.customerName,
                    style = MaterialTheme.typography.bodyMedium,
                    maxLines = 1
                )
                Text(
                    text = appointment.serviceType.replaceFirstChar { it.uppercase() },
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            
            // Status
            Surface(
                color = when(appointment.status) {
                    AppointmentStatus.CONFIRMED -> Color(0xFF4CAF50).copy(alpha = 0.2f)
                    AppointmentStatus.COMPLETED -> PSDBlue.copy(alpha = 0.2f)
                    AppointmentStatus.CANCELLED -> Color(0xFFF44336).copy(alpha = 0.2f)
                    else -> Color(0xFFFF9800).copy(alpha = 0.2f)
                },
                shape = RoundedCornerShape(4.dp)
            ) {
                Text(
                    text = appointment.status.name.lowercase().replaceFirstChar { it.uppercase() },
                    style = MaterialTheme.typography.labelSmall,
                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                )
            }
        }
    }
}
