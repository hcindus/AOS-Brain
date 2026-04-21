package com.ps.pos.data.dao

import androidx.room.*
import com.ps.pos.data.entities.Transaction
import kotlinx.coroutines.flow.Flow

@Dao
interface TransactionDao {
    @Query("SELECT * FROM transactions ORDER BY timestamp DESC")
    fun getAllTransactions(): Flow<List<Transaction>>

    @Query("SELECT * FROM transactions WHERE id = :id LIMIT 1")
    suspend fun getById(id: Long): Transaction?

    @Query("SELECT * FROM transactions WHERE date(timestamp/1000, 'unixepoch') = date('now') ORDER BY timestamp DESC")
    fun getTodayTransactions(): Flow<List<Transaction>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(transaction: Transaction): Long

    @Query("UPDATE transactions SET status = 'VOIDED' WHERE id = :id")
    suspend fun voidTransaction(id: Long)

    @Query("SELECT SUM(total) FROM transactions WHERE date(timestamp/1000, 'unixepoch') = date('now') AND status = 'COMPLETED'")
    suspend fun getTodaySales(): Double?
}