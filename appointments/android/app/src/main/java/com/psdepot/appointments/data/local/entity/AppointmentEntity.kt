package com.psdepot.appointments.data.local.entity

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey
import com.psdepot.appointments.data.model.Appointment
import com.psdepot.appointments.data.model.AppointmentStatus
import com.psdepot.appointments.data.model.LeadInfo
import java.time.LocalDateTime

@Entity(tableName = "appointments")
data class AppointmentEntity(
    @PrimaryKey
    @ColumnInfo(name = "id")
    val id: String,
    
    @ColumnInfo(name = "lead_id")
    val leadId: Int? = null,
    
    @ColumnInfo(name = "customer_name")
    val customerName: String,
    
    @ColumnInfo(name = "customer_email")
    val customerEmail: String? = null,
    
    @ColumnInfo(name = "customer_phone")
    val customerPhone: String? = null,
    
    @ColumnInfo(name = "service_type")
    val serviceType: String = "consultation",
    
    @ColumnInfo(name = "scheduled_at")
    val scheduledAt: String, // ISO 8601 format
    
    @ColumnInfo(name = "duration_minutes")
    val durationMinutes: Int = 60,
    
    @ColumnInfo(name = "status")
    val status: String = "CONFIRMED",
    
    @ColumnInfo(name = "notes")
    val notes: String? = null,
    
    @ColumnInfo(name = "google_event_id")
    val googleEventId: String? = null,
    
    @ColumnInfo(name = "reminder_sent")
    val reminderSent: Boolean = false,
    
    @ColumnInfo(name = "synced_at")
    val syncedAt: Long = System.currentTimeMillis()
) {
    fun toAppointment(): Appointment {
        return Appointment(
            id = id,
            leadId = leadId,
            customerName = customerName,
            customerEmail = customerEmail,
            customerPhone = customerPhone,
            serviceType = serviceType,
            scheduledAt = LocalDateTime.parse(scheduledAt),
            durationMinutes = durationMinutes,
            status = AppointmentStatus.valueOf(status),
            notes = notes,
            googleEventId = googleEventId,
            reminderSent = reminderSent
        )
    }
    
    companion object {
        fun fromAppointment(appointment: Appointment): AppointmentEntity {
            return AppointmentEntity(
                id = appointment.id,
                leadId = appointment.leadId,
                customerName = appointment.customerName,
                customerEmail = appointment.customerEmail,
                customerPhone = appointment.customerPhone,
                serviceType = appointment.serviceType,
                scheduledAt = appointment.scheduledAt.toString(),
                durationMinutes = appointment.durationMinutes,
                status = appointment.status.name,
                notes = appointment.notes,
                googleEventId = appointment.googleEventId,
                reminderSent = appointment.reminderSent
            )
        }
    }
}

@Entity(tableName = "leads_cache")
data class LeadEntity(
    @PrimaryKey
    @ColumnInfo(name = "id")
    val id: Int,
    
    @ColumnInfo(name = "company_name")
    val companyName: String? = null,
    
    @ColumnInfo(name = "contact_name")
    val contactName: String? = null,
    
    @ColumnInfo(name = "phone")
    val phone: String? = null,
    
    @ColumnInfo(name = "email")
    val email: String? = null,
    
    @ColumnInfo(name = "county")
    val county: String? = null,
    
    @ColumnInfo(name = "state")
    val state: String? = null,
    
    @ColumnInfo(name = "cached_at")
    val cachedAt: Long = System.currentTimeMillis()
) {
    fun toLeadInfo(): LeadInfo {
        return LeadInfo(
            id = id,
            companyName = companyName,
            contactName = contactName,
            phone = phone,
            email = email,
            county = county,
            state = state
        )
    }
}

@Entity(tableName = "sync_queue")
data class SyncQueueEntity(
    @PrimaryKey(autoGenerate = true)
    @ColumnInfo(name = "id")
    val id: Long = 0,
    
    @ColumnInfo(name = "operation")
    val operation: String, // CREATE, UPDATE, DELETE
    
    @ColumnInfo(name = "entity_type")
    val entityType: String, // APPOINTMENT, LEAD, etc
    
    @ColumnInfo(name = "entity_id")
    val entityId: String,
    
    @ColumnInfo(name = "payload")
    val payload: String?, // JSON data
    
    @ColumnInfo(name = "created_at")
    val createdAt: Long = System.currentTimeMillis(),
    
    @ColumnInfo(name = "retry_count")
    val retryCount: Int = 0,
    
    @ColumnInfo(name = "last_error")
    val lastError: String? = null
)
