package com.psdepot.appointments.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.psdepot.appointments.data.model.Appointment
import com.psdepot.appointments.data.model.AppointmentStatus
import com.psdepot.appointments.data.repository.AppointmentRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import java.time.LocalDate
import java.time.LocalDateTime
import javax.inject.Inject

@HiltViewModel
class AppointmentsListViewModel @Inject constructor(
    private val appointmentRepository: AppointmentRepository
) : ViewModel() {

    private val _appointments = MutableStateFlow<List<Appointment>>(emptyList())
    val appointments: StateFlow<List<Appointment>> = _appointments.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    private val _selectedFilter = MutableStateFlow<FilterOption>(FilterOption.ALL)
    val selectedFilter: StateFlow<FilterOption> = _selectedFilter.asStateFlow()

    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error.asStateFlow()

    private var allAppointments: List<Appointment> = emptyList()

    init {
        loadAppointments()
    }

    fun loadAppointments() {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null

            val result = appointmentRepository.getBookings(perPage = 100)
            
            result.onSuccess { response ->
                allAppointments = response.appointments
                applyFilter()
            }.onFailure { error ->
                _error.value = "Failed to load appointments: ${error.message}"
            }

            _isLoading.value = false
        }
    }

    fun setFilter(filter: FilterOption) {
        _selectedFilter.value = filter
        applyFilter()
    }

    private fun applyFilter() {
        val now = LocalDateTime.now()
        
        _appointments.value = when (_selectedFilter.value) {
            FilterOption.ALL -> allAppointments
            FilterOption.CONFIRMED -> allAppointments.filter { it.status == AppointmentStatus.CONFIRMED }
            FilterOption.COMPLETED -> allAppointments.filter { it.status == AppointmentStatus.COMPLETED }
            FilterOption.CANCELLED -> allAppointments.filter { it.status == AppointmentStatus.CANCELLED }
            FilterOption.UPCOMING -> allAppointments.filter { it.scheduledAt.isAfter(now) }
            FilterOption.PAST -> allAppointments.filter { it.scheduledAt.isBefore(now) }
        }
    }

    fun refresh() {
        loadAppointments()
    }

    fun clearError() {
        _error.value = null
    }

    enum class FilterOption {
        ALL, CONFIRMED, COMPLETED, CANCELLED, UPCOMING, PAST
    }
}
