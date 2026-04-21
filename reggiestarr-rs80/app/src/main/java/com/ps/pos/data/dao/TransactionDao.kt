package com.ps.pos.data.dao

import androidx.room.*
import com.ps.pos.data.entities.Transaction
import kotlinx.coroutines.flow.Flow

@Dao
interface TransactionDao {
    @Query("SELECT * FROM transactions ORDER BY timestamp DESC")
    fun getAll(): Flow<List<Transaction>>

    @Query("SELECT * FROM transactions WHERE timestamp > :since ORDER BY timestamp DESC")
    fun getSince(since: Long): Flow<List<Transaction>>

    @Query("SELECT * FROM transactions WHERE id = :id LIMIT 1")
    suspend fun getById(id: String): Transaction?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(transaction: Transaction): Long

    @Query("UPDATE transactions SET status = 'VOIDED' WHERE id = :id")
    suspend fun void(id: String)

    @Query("SELECT SUM(total) FROM transactions WHERE status = 'COMPLETED' AND timestamp > :since")
    suspend fun getTotalSince(since: Long): Double?

    @Query("SELECT COUNT(*) FROM transactions WHERE timestamp > :since")
    suspend fun getCountSince(since: Long): Int?
}
