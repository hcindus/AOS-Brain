package com.psdepot.appointments.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.psdepot.appointments.data.model.Appointment
import com.psdepot.appointments.data.model.AppointmentStatus
import com.psdepot.appointments.data.model.AvailabilitySlot
import com.psdepot.appointments.data.repository.AppointmentRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import java.time.LocalDate
import java.time.LocalTime
import javax.inject.Inject

@HiltViewModel
class CalendarViewModel @Inject constructor(
    private val repository: AppointmentRepository
) : ViewModel() {

    private val _selectedDate = MutableStateFlow(LocalDate.now())
    val selectedDate: StateFlow<LocalDate> = _selectedDate.asStateFlow()

    private val _availabilitySlots = MutableStateFlow<List<AvailabilitySlot>>(emptyList())
    val availabilitySlots: StateFlow<List<AvailabilitySlot>> = _availabilitySlots.asStateFlow()

    private val _appointments = MutableStateFlow<List<Appointment>>(emptyList())
    val appointments: StateFlow<List<Appointment>> = _appointments.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error.asStateFlow()

    init {
        loadData()
    }

    fun selectDate(date: LocalDate) {
        _selectedDate.value = date
        loadData()
    }

    fun previousWeek() {
        _selectedDate.value = _selectedDate.value.minusWeeks(1)
        loadData()
    }

    fun nextWeek() {
        _selectedDate.value = _selectedDate.value.plusWeeks(1)
        loadData()
    }

    fun loadData() {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null
            
            try {
                // Load availability slots for selected date
                val slotsResult = repository.getAvailability(
                    date = _selectedDate.value.toString(),
                    days = 7
                )
                
                slotsResult.onSuccess { response ->
                    _availabilitySlots.value = response.slots
                }.onFailure { error ->
                    _error.value = "Failed to load availability: ${error.message}"
                }

                // Load appointments for the week
                val startOfWeek = _selectedDate.value.minusDays(_selectedDate.value.dayOfWeek.value.toLong() - 1)
                val endOfWeek = startOfWeek.plusDays(6)
                
                val bookingsResult = repository.getBookings(
                    startDate = startOfWeek.toString(),
                    endDate = endOfWeek.toString(),
                    perPage = 100
                )
                
                bookingsResult.onSuccess { response ->
                    _appointments.value = response.appointments
                }.onFailure { error ->
                    _error.value = "Failed to load appointments: ${error.message}"
                }
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun refresh() {
        loadData()
    }

    fun clearError() {
        _error.value = null
    }

    // Generate default time slots for demo/testing
    private fun generateDefaultSlots(): List<AvailabilitySlot> {
        val slots = mutableListOf<AvailabilitySlot>()
        val startTime = LocalTime.of(8, 0)
        val endTime = LocalTime.of(17, 0)
        var currentTime = startTime
        
        while (currentTime.isBefore(endTime)) {
            slots.add(
                AvailabilitySlot(
                    id = slots.size + 1,
                    slotDate = _selectedDate.value,
                    slotTime = currentTime,
                    isAvailable = true
                )
            )
            currentTime = currentTime.plusMinutes(30)
        }
        
        return slots
    }
}
