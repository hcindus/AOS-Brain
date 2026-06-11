package com.psdepot.appointments.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.psdepot.appointments.data.model.LeadInfo
import com.psdepot.appointments.data.remote.api.CreateBookingRequest
import com.psdepot.appointments.data.repository.AppointmentRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.LocalTime
import java.time.format.DateTimeFormatter
import javax.inject.Inject

@HiltViewModel
class BookingViewModel @Inject constructor(
    private val appointmentRepository: AppointmentRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(BookingUiState())
    val uiState: StateFlow<BookingUiState> = _uiState.asStateFlow()

    private val _selectedLead = MutableStateFlow<LeadInfo?>(null)
    val selectedLead: StateFlow<LeadInfo?> = _selectedLead.asStateFlow()

    fun setSelectedLead(lead: LeadInfo?) {
        _selectedLead.value = lead
        lead?.let {
            _uiState.value = _uiState.value.copy(
                customerName = it.contactName ?: it.companyName ?: "",
                customerEmail = it.email ?: "",
                customerPhone = it.phone ?: ""
            )
        }
    }

    fun clearSelectedLead() {
        _selectedLead.value = null
        _uiState.value = _uiState.value.copy(
            customerName = "",
            customerEmail = "",
            customerPhone = ""
        )
    }

    fun onCustomerNameChange(name: String) {
        _uiState.value = _uiState.value.copy(customerName = name)
    }

    fun onCustomerEmailChange(email: String) {
        _uiState.value = _uiState.value.copy(customerEmail = email)
    }

    fun onCustomerPhoneChange(phone: String) {
        _uiState.value = _uiState.value.copy(customerPhone = phone)
    }

    fun onServiceTypeChange(serviceType: String) {
        _uiState.value = _uiState.value.copy(serviceType = serviceType)
    }

    fun onDateChange(date: LocalDate) {
        _uiState.value = _uiState.value.copy(selectedDate = date)
    }

    fun onTimeChange(time: LocalTime) {
        _uiState.value = _uiState.value.copy(selectedTime = time)
    }

    fun onDurationChange(minutes: Int) {
        _uiState.value = _uiState.value.copy(durationMinutes = minutes)
    }

    fun onNotesChange(notes: String) {
        _uiState.value = _uiState.value.copy(notes = notes)
    }

    fun submitBooking() {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true, error = null)

            val state = _uiState.value
            val scheduledAt = LocalDateTime.of(
                state.selectedDate,
                state.selectedTime
            )

            val request = CreateBookingRequest(
                lead_id = _selectedLead.value?.id,
                customer_name = state.customerName,
                customer_email = state.customerEmail.takeIf { it.isNotBlank() },
                customer_phone = state.customerPhone.takeIf { it.isNotBlank() },
                service_type = state.serviceType,
                scheduled_at = scheduledAt.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME),
                duration_minutes = state.durationMinutes,
                notes = state.notes.takeIf { it.isNotBlank() }
            )

            appointmentRepository.createBooking(request)
                .onSuccess { appointmentId ->
                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        isSuccess = true,
                        createdAppointmentId = appointmentId
                    )
                }
                .onFailure { error ->
                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        error = error.message ?: "Failed to create booking"
                    )
                }
        }
    }

    fun clearError() {
        _uiState.value = _uiState.value.copy(error = null)
    }

    data class BookingUiState(
        val customerName: String = "",
        val customerEmail: String = "",
        val customerPhone: String = "",
        val serviceType: String = "consultation",
        val selectedDate: LocalDate = LocalDate.now(),
        val selectedTime: LocalTime = LocalTime.of(9, 0),
        val durationMinutes: Int = 60,
        val notes: String = "",
        val isLoading: Boolean = false,
        val isSuccess: Boolean = false,
        val error: String? = null,
        val createdAppointmentId: String? = null
    ) {
        val canSubmit: Boolean
            get() = customerName.isNotBlank()
    }
}
