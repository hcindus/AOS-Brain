package com.ps.pos.data.dao

import androidx.room.*
import com.ps.pos.data.entities.LineItem
import kotlinx.coroutines.flow.Flow

@Dao
interface LineItemDao {
    @Query("SELECT * FROM line_items WHERE transactionId = :transactionId")
    fun getByTransactionId(transactionId: Long): Flow<List<LineItem>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(lineItem: LineItem)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(lineItems: List<LineItem>)

    @Update
    suspend fun update(lineItem: LineItem)

    @Delete
    suspend fun delete(lineItem: LineItem)
}