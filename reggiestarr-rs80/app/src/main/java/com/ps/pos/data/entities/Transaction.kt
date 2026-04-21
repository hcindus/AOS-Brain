package com.ps.pos.data.entities

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.util.Date

@Entity(tableName = "transactions")
data class Transaction(
    @PrimaryKey val id: String = java.util.UUID.randomUUID().toString(),
    val timestamp: Long = Date().time,
    val subtotal: Double = 0.0,
    val taxAmount: Double = 0.0,
    val total: Double = 0.0,
    val paymentType: String = "CASH",
    val tendered: Double = 0.0,
    val change: Double = 0.0,
    val status: String = "COMPLETED", // COMPLETED, VOIDED, HELD
    val receiptPrinted: Boolean = false
)
