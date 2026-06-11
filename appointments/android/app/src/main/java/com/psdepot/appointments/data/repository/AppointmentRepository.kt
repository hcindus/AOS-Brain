package com.psdepot.appointments.data.repository

import com.psdepot.appointments.data.local.dao.AppointmentDao
import com.psdepot.appointments.data.local.entity.AppointmentEntity
import com.psdepot.appointments.data.model.Appointment
import com.psdepot.appointments.data.model.AvailabilitySlot
import com.psdepot.appointments.data.remote.api.AppointmentApi
import com.psdepot.appointments.data.remote.api.AvailabilityResponse
import com.psdepot.appointments.data.remote.api.BookingsResponse
import com.psdepot.appointments.data.remote.api.CreateBookingRequest
import com.psdepot.appointments.data.remote.api.LeadsSearchResponse
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import retrofit2.HttpException
import java.io.IOException
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AppointmentRepository @Inject constructor(
    private val api: AppointmentApi,
    private val appointmentDao: AppointmentDao? = null
) {

    suspend fun getAvailability(
        date: String? = null,
        days: Int = 7,
        serviceType: String? = null
    ): Result<AvailabilityResponse> = withContext(Dispatchers.IO) {
        try {
            val response = api.getAvailability(date, days, serviceType)
            if (response.isSuccessful) {
                Result.success(response.body()!!)
            } else {
                Result.failure(HttpException(response))
            }
        } catch (e: IOException) {
            Result.failure(e)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getBookings(
        page: Int = 1,
        perPage: Int = 50,
        status: String? = null,
        startDate: String? = null,
        endDate: String? = null
    ): Result<BookingsResponse> = withContext(Dispatchers.IO) {
        try {
            val response = api.getBookings(page, perPage, status, startDate, endDate)
            if (response.isSuccessful) {
                response.body()?.let {
                    // Cache to local database
                    appointmentDao?.let { dao ->
                        it.appointments.map { appt ->
                            AppointmentEntity.fromAppointment(appt)
                        }.forEach { entity ->
                            dao.insertAppointment(entity)
                        }
                    }
                    Result.success(it)
                } ?: Result.failure(Exception("Empty response body"))
            } else {
                Result.failure(HttpException(response))
            }
        } catch (e: IOException) {
            // Try to load from cache
            val cachedAppointments = appointmentDao?.let { dao ->
                val entities = if (startDate != null && endDate != null) {
                    dao.getAppointmentsBetween(startDate, endDate)
                } else {
                    dao.getAllAppointments()
                }
                entities.map { it.toAppointment() }
            } ?: emptyList()
            
            if (cachedAppointments.isNotEmpty()) {
                Result.success(BookingsResponse(
                    appointments = cachedAppointments,
                    total = cachedAppointments.size,
                    page = page,
                    per_page = perPage,
                    pages = 1
                ))
            } else {
                Result.failure(e)
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getBookingDetail(appointmentId: String): Result<Appointment> = withContext(Dispatchers.IO) {
        try {
            val response = api.getBookingDetail(appointmentId)
            if (response.isSuccessful) {
                response.body()?.let {
                    Result.success(it)
                } ?: Result.failure(Exception("Empty response body"))
            } else {
                Result.failure(HttpException(response))
            }
        } catch (e: IOException) {
            // Try cache
            appointmentDao?.getAppointmentById(appointmentId)?.let {
                Result.success(it.toAppointment())
            } ?: Result.failure(e)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun createBooking(request: CreateBookingRequest): Result<String> = withContext(Dispatchers.IO) {
        try {
            val response = api.createBooking(request)
            if (response.isSuccessful) {
                response.body()?.let {
                    Result.success(it.appointment_id)
                } ?: Result.failure(Exception("Empty response body"))
            } else {
                val errorMsg = response.errorBody()?.string() ?: "Unknown error"
                Result.failure(Exception("Failed to create booking: $errorMsg"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun updateBooking(
        appointmentId: String,
        status: String? = null,
        notes: String? = null
    ): Result<Boolean> = withContext(Dispatchers.IO) {
        try {
            val request = com.psdepot.appointments.data.remote.api.UpdateBookingRequest(
                status = status,
                notes = notes
            )
            val response = api.updateBooking(appointmentId, request)
            if (response.isSuccessful) {
                Result.success(true)
            } else {
                Result.failure(HttpException(response))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun cancelBooking(appointmentId: String): Result<Boolean> = withContext(Dispatchers.IO) {
        try {
            val response = api.cancelBooking(appointmentId)
            if (response.isSuccessful) {
                // Update local cache
                appointmentDao?.updateAppointmentStatus(appointmentId, "CANCELLED")
                Result.success(true)
            } else {
                Result.failure(HttpException(response))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun searchLeads(query: String): Result<LeadsSearchResponse> = withContext(Dispatchers.IO) {
        try {
            val response = api.searchLeads(query)
            if (response.isSuccessful) {
                response.body()?.let {
                    Result.success(it)
                } ?: Result.failure(Exception("Empty response body"))
            } else {
                Result.failure(HttpException(response))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun checkHealth(): Result<Map<String, String>> = withContext(Dispatchers.IO) {
        try {
            val response = api.checkHealth()
            if (response.isSuccessful) {
                Result.success(response.body() ?: emptyMap())
            } else {
                Result.failure(HttpException(response))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
