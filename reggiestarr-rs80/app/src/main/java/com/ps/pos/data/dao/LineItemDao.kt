package com.ps.pos.data.dao

import androidx.room.*
import com.ps.pos.data.entities.LineItem
import kotlinx.coroutines.flow.Flow

@Dao
interface LineItemDao {
    @Query("SELECT * FROM line_items WHERE transactionId = :txId")
    fun getForTransaction(txId: String): Flow<List<LineItem>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(item: LineItem)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(items: List<LineItem>)

    @Delete
    suspend fun delete(item: LineItem)

    @Query("DELETE FROM line_items WHERE transactionId = :txId")
    suspend fun deleteForTransaction(txId: String)
}
