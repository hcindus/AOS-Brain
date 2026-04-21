package com.ps.pos.data.entities

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "line_items")
data class LineItem(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val transactionId: Long? = null,
    val productId: Long,
    val productName: String,
    val quantity: Double,
    val unitPrice: Double,
    val totalPrice: Double,
    val isVoided: Boolean = false
)