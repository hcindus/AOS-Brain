package com.psdepot.appointments.ui.screens.mobile

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
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
import java.time.format.DateTimeFormatter

/**
 * Mobile-optimized calendar view
 * Features: Week strip at top, vertical time slots list
 */
@Composable
fun MobileCalendarContent(
    onAppointmentClick: (String) -> Unit,
    onSearchLeads: () -> Unit,
    modifier: Modifier = Modifier,
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

    Column(modifier = modifier.fillMaxSize()) {
        // Week strip - horizontal scrollable
        WeekStrip(
            weekDays = weekDays,
            selectedDate = selectedDate,
            onDateSelected = { viewModel.selectDate(it) },
            onPreviousWeek = { viewModel.previousWeek() },
            onNextWeek = { viewModel.nextWeek() }
        )
        
        // Selected date header
        Text(
            text = selectedDate.format(DateTimeFormatter.ofPattern("EEEE, MMMM d")),
            style = MaterialTheme.typography.titleMedium,
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
        )
        
        Divider()
        
        // Time slots
        if (isLoading) {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                CircularProgressIndicator(color = PSDOrange)
            }
        } else {
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                verticalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                items(availabilitySlots) { slot ->
                    val appointment = appointments.find { 
                        it.scheduledAt.toLocalDate() == slot.slotDate &&
                        it.scheduledAt.toLocalTime() == slot.slotTime
                    }
                    
                    MobileTimeSlotCard(
                        slot = slot,
                        appointment = appointment,
                        onClick = { 
                            appointment?.let { onAppointmentClick(it.id) }
                                ?: onSearchLeads()
                        }
                    )
                }
            }
        }
    }
}

@Composable
fun WeekStrip(
    weekDays: List<LocalDate>,
    selectedDate: LocalDate,
    onDateSelected: (LocalDate) -> Unit,
    onPreviousWeek: () -> Unit,
    onNextWeek: () -> Unit
) {
    Surface(
        tonalElevation = 2.dp,
        color = MaterialTheme.colorScheme.surface
    ) {
        Column {
            // Month/Year header with nav arrows
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
                
                Text(
                    text = selectedDate.format(DateTimeFormatter.ofPattern("MMMM yyyy")),
                    style = MaterialTheme.typography.titleMedium
                )
                
                IconButton(onClick = onNextWeek) {
                    Icon(Icons.Default.ArrowForward, contentDescription = "Next week")
                }
            }
            
            // Days of week
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 8.dp, vertical = 4.dp),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                weekDays.forEach { date ->
                    val isSelected = date == selectedDate
                    val isToday = date == LocalDate.now()
                    
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        modifier = Modifier
                            .clip(RoundedCornerShape(12.dp))
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
                            text = date.dayOfWeek.name.take(1),
                            style = MaterialTheme.typography.bodySmall,
                            color = when {
                                isSelected -> Color.White
                                else -> MaterialTheme.colorScheme.onSurface
                            }
                        )
                        Text(
                            text = date.dayOfMonth.toString(),
                            style = MaterialTheme.typography.titleMedium,
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
fun MobileTimeSlotCard(
    slot: AvailabilitySlot,
    appointment: Appointment?,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        colors = CardDefaults.cardColors(
            containerColor = when {
                appointment != null -> PSDOrange.copy(alpha = 0.1f)
                slot.isAvailable -> MaterialTheme.colorScheme.surface
                else -> MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
            }
        )
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Time
            Text(
                text = slot.slotTime.format(DateTimeFormatter.ofPattern("h:mm a")),
                style = MaterialTheme.typography.bodyLarge,
                modifier = Modifier.width(70.dp)
            )
            
            Spacer(modifier = Modifier.width(16.dp))
            
            // Content
            when {
                appointment != null -> {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = appointment.customerName,
                            style = MaterialTheme.typography.bodyLarge,
                            maxLines = 1
                        )
                        Text(
                            text = appointment.serviceType.replaceFirstChar { it.uppercase() },
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                    
                    // Status indicator
                    Surface(
                        color = when(appointment.status) {
                            AppointmentStatus.CONFIRMED -> Color(0xFF4CAF50)
                            AppointmentStatus.COMPLETED -> PSDBlue
                            AppointmentStatus.CANCELLED -> Color(0xFFF44336)
                            else -> Color(0xFFFF9800)
                        },
                        shape = RoundedCornerShape(4.dp),
                        modifier = Modifier.size(8.dp)
                    ) {}
                }
                slot.isAvailable -> {
                    Text(
                        text = "Available",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.primary,
                        modifier = Modifier.weight(1f)
                    )
                }
                else -> {
                    Text(
                        text = "—",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.weight(1f)
                    )
                }
            }
        }
    }
}
