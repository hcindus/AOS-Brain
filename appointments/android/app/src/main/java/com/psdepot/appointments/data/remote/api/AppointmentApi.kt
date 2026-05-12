package com.psdepot.appointments.data.remote.api

import com.psdepot.appointments.data.model.Appointment
import com.psdepot.appointments.data.model.AvailabilitySlot
import com.psdepot.appointments.data.model.LeadInfo
import retrofit2.Response
import retrofit2.http.*

interface AppointmentApi {
    
    @GET("health")
    suspend fun checkHealth(): Response<Map<String, String>>
    
    @GET("api/v1/availability")
    suspend fun getAvailability(
        @Query("date") date: String? = null,
        @Query("days") days: Int = 7,
        @Query("service_type") serviceType: String? = null
    ): Response<AvailabilityResponse>
    
    @POST("api/v1/bookings")
    suspend fun createBooking(
        @Body request: CreateBookingRequest
    ): Response<CreateBookingResponse>
    
    @GET("api/v1/bookings")
    suspend fun getBookings(
        @Query("page") page: Int = 1,
        @Query("per_page") perPage: Int = 50,
        @Query("status") status: String? = null,
        @Query("start_date") startDate: String? = null,
        @Query("end_date") endDate: String? = null
    ): Response<BookingsResponse>
    
    @GET("api/v1/bookings/{id}")
    suspend fun getBookingDetail(
        @Path("id") appointmentId: String
    ): Response<Appointment>
    
    @PUT("api/v1/bookings/{id}")
    suspend fun updateBooking(
        @Path("id") appointmentId: String,
        @Body request: UpdateBookingRequest
    ): Response<UpdateResponse>
    
    @DELETE("api/v1/bookings/{id}")
    suspend fun cancelBooking(
        @Path("id") appointmentId: String
    ): Response<DeleteResponse>
    
    @GET("api/v1/leads/search")
    suspend fun searchLeads(
        @Query("q") query: String
    ): Response<LeadsSearchResponse>
}

// Request/Response data classes
data class CreateBookingRequest(
    val lead_id: Int? = null,
    val customer_name: String,
    val customer_email: String? = null,
    val customer_phone: String? = null,
    val service_type: String = "consultation",
    val scheduled_at: String,  // ISO 8601 format
    val duration_minutes: Int = 60,
    val notes: String? = null
)

data class CreateBookingResponse(
    val success: Boolean,
    val appointment_id: String,
    val message: String
)

data class UpdateBookingRequest(
    val status: String? = null,
    val notes: String? = null,
    val customer_name: String? = null,
    val customer_email: String? = null,
    val customer_phone: String? = null,
    val scheduled_at: String? = null,
    val duration_minutes: Int? = null
)

data class UpdateResponse(
    val success: Boolean,
    val updated: Int
)

data class DeleteResponse(
    val success: Boolean,
    val deleted: Int
)

data class AvailabilityResponse(
    val slots: List<AvailabilitySlot>,
    val count: Int,
    val date: String?,
    val days_requested: Int
)

data class BookingsResponse(
    val appointments: List<Appointment>,
    val total: Int,
    val page: Int,
    val per_page: Int,
    val pages: Int
)

data class LeadsSearchResponse(
    val leads: List<LeadInfo>,
    val count: Int
)