package com.psdepot.appointments.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.psdepot.appointments.data.model.Appointment
import com.psdepot.appointments.data.repository.AppointmentRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class AppointmentDetailViewModel @Inject constructor(
    private val appointmentRepository: AppointmentRepository
) : ViewModel() {

    private val _appointment = MutableStateFlow<Appointment?>(null)
    val appointment: StateFlow<Appointment?> = _appointment.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    private val _showCancelDialog = MutableStateFlow(false)
    val showCancelDialog: StateFlow<Boolean> = _showCancelDialog.asStateFlow()

    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error.asStateFlow()

    fun loadAppointment(appointmentId: String) {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null

            appointmentRepository.getBookingDetail(appointmentId)
                .onSuccess { appointment ->
                    _appointment.value = appointment
                }
                .onFailure { error ->
                    _error.value = "Failed to load appointment: ${error.message}"
                }

            _isLoading.value = false
        }
    }

    fun showCancelDialog() {
        _showCancelDialog.value = true
    }

    fun dismissCancelDialog() {
        _showCancelDialog.value = false
    }

    fun cancelAppointment() {
        viewModelScope.launch {
            _appointment.value?.let { appointment ->
                _isLoading.value = true

                appointmentRepository.cancelBooking(appointment.id)
                    .onSuccess {
                        // Refresh appointment data
                        loadAppointment(appointment.id)
                    }
                    .onFailure { error ->
                        _error.value = "Failed to cancel: ${error.message}"
                    }

                _showCancelDialog.value = false
                _isLoading.value = false
            }
        }
    }

    fun markComplete() {
        viewModelScope.launch {
            _appointment.value?.let { appointment ->
                _isLoading.value = true

                appointmentRepository.updateBooking(
                    appointmentId = appointment.id,
                    status = "COMPLETED"
                )
                    .onSuccess {
                        // Refresh appointment data
                        loadAppointment(appointment.id)
                    }
                    .onFailure { error ->
                        _error.value = "Failed to mark complete: ${error.message}"
                    }

                _isLoading.value = false
            }
        }
    }

    fun clearError() {
        _error.value = null
    }
}
