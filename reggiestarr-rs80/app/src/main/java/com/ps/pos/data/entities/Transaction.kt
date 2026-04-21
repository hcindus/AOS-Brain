package com.ps.pos.data.entities

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "transactions")
data class Transaction(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val transactionNumber: String,
    val timestamp: Long,
    val subtotal: Double,
    val tax: Double,
    val total: Double,
    val paymentType: String,
    val tendered: Double,
    val change: Double,
    val status: String // COMPLETED, VOIDED, REFUNDED
)