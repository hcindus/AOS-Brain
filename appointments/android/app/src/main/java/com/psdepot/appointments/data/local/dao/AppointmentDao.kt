package com.psdepot.appointments.data.local.dao

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Transaction
import androidx.room.Update
import com.psdepot.appointments.data.local.entity.AppointmentEntity
import com.psdepot.appointments.data.local.entity.LeadEntity
import com.psdepot.appointments.data.local.entity.SyncQueueEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface AppointmentDao {
    @Query("SELECT * FROM appointments ORDER BY scheduled_at DESC")
    fun getAllAppointments(): Flow<List<AppointmentEntity>>
    
    @Query("SELECT * FROM appointments WHERE scheduled_at BETWEEN :startDate AND :endDate ORDER BY scheduled_at ASC")
    suspend fun getAppointmentsBetween(startDate: String, endDate: String): List<AppointmentEntity>
    
    @Query("SELECT * FROM appointments WHERE scheduled_at LIKE :datePattern || '%' ORDER BY scheduled_at ASC")
    suspend fun getAppointmentsForDate(datePattern: String): List<AppointmentEntity>
    
    @Query("SELECT * FROM appointments WHERE id = :appointmentId LIMIT 1")
    suspend fun getAppointmentById(appointmentId: String): AppointmentEntity?
    
    @Query("SELECT * FROM appointments WHERE status = :status ORDER BY scheduled_at DESC")
    fun getAppointmentsByStatus(status: String): Flow<List<AppointmentEntity>>
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAppointment(appointment: AppointmentEntity)
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAppointments(appointments: List<AppointmentEntity>)
    
    @Update
    suspend fun updateAppointment(appointment: AppointmentEntity)
    
    @Query("UPDATE appointments SET status = :status WHERE id = :appointmentId")
    suspend fun updateAppointmentStatus(appointmentId: String, status: String)
    
    @Delete
    suspend fun deleteAppointment(appointment: AppointmentEntity)
    
    @Query("DELETE FROM appointments WHERE id = :appointmentId")
    suspend fun deleteAppointmentById(appointmentId: String)
    
    @Query("DELETE FROM appointments WHERE synced_at < :timestamp")
    suspend fun deleteOldAppointments(timestamp: Long)
    
    @Query("SELECT COUNT(*) FROM appointments")
    suspend fun getAppointmentCount(): Int
}

@Dao
interface LeadDao {
    @Query("SELECT * FROM leads_cache ORDER BY contact_name, company_name")
    fun getAllLeads(): Flow<List<LeadEntity>>
    
    @Query("SELECT * FROM leads_cache WHERE contact_name LIKE '%' || :query || '%' OR company_name LIKE '%' || :query || '%' OR email LIKE '%' || :query || '%'")
    suspend fun searchLeads(query: String): List<LeadEntity>
    
    @Query("SELECT * FROM leads_cache WHERE id = :leadId LIMIT 1")
    suspend fun getLeadById(leadId: Int): LeadEntity?
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertLead(lead: LeadEntity)
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertLeads(leads: List<LeadEntity>)
    
    @Query("DELETE FROM leads_cache WHERE cached_at < :timestamp")
    suspend fun deleteOldLeads(timestamp: Long)
    
    @Query("DELETE FROM leads_cache")
    suspend fun clearAllLeads()
}

@Dao
interface SyncQueueDao {
    @Query("SELECT * FROM sync_queue ORDER BY created_at ASC")
    suspend fun getAllPendingOperations(): List<SyncQueueEntity>
    
    @Query("SELECT * FROM sync_queue WHERE entity_type = :entityType ORDER BY created_at ASC")
    suspend fun getPendingOperationsForEntity(entityType: String): List<SyncQueueEntity>
    
    @Insert
    suspend fun insertOperation(operation: SyncQueueEntity): Long
    
    @Query("UPDATE sync_queue SET retry_count = retry_count + 1, last_error = :error WHERE id = :operationId")
    suspend fun incrementRetryCount(operationId: Long, error: String?)
    
    @Query("DELETE FROM sync_queue WHERE id = :operationId")
    suspend fun deleteOperation(operationId: Long)
    
    @Query("DELETE FROM sync_queue WHERE retry_count > 5")
    suspend fun deleteFailedOperations()
    
    @Query("SELECT COUNT(*) FROM sync_queue")
    suspend fun getPendingCount(): Int
    
    @Query("SELECT * FROM sync_queue WHERE id = :operationId LIMIT 1")
    suspend fun getOperationById(operationId: Long): SyncQueueEntity?
}
