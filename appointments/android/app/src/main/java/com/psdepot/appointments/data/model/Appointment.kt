package com.psdepot.appointments.data.model

import java.time.LocalDateTime

data class Appointment(
    val id: String,
    val leadId: Int? = null,
    val customerName: String,
    val customerEmail: String? = null,
    val customerPhone: String? = null,
    val serviceType: String = "consultation",
    val scheduledAt: LocalDateTime,
    val durationMinutes: Int = 60,
    val status: AppointmentStatus = AppointmentStatus.CONFIRMED,
    val notes: String? = null,
    val googleEventId: String? = null,
    val reminderSent: Boolean = false,
    val leadInfo: LeadInfo? = null
) {
    // Extension helper for LocalDate extraction
    fun getScheduledDate(): java.time.LocalDate = scheduledAt.toLocalDate()
    fun getScheduledTime(): java.time.LocalTime = scheduledAt.toLocalTime()
}

enum class AppointmentStatus {
    CONFIRMED,
    COMPLETED,
    CANCELLED,
    NO_SHOW
}

data class LeadInfo(
    val id: Int,
    val companyName: String? = null,
    val contactName: String? = null,
    val phone: String? = null,
    val email: String? = null,
    val county: String? = null,
    val state: String? = null
) {
    fun toDisplayName(): String {
        return contactName ?: companyName ?: "Unknown"
    }
}

data class AvailabilitySlot(
    val id: Int,
    val slotDate: java.time.LocalDate,
    val slotTime: java.time.LocalTime,
    val durationMinutes: Int = 60,
    val isAvailable: Boolean = true,
    val appointmentId: String? = null,
    val bufferBefore: Int = 15,
    val bufferAfter: Int = 15
)

data class ServiceType(
    val id: String,
    val name: String,
    val durationMinutes: Int,
    val color: String? = null,
    val description: String? = null,
    val requiresLead: Boolean = true
)