package com.ps.pos.data.entities

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "line_items")
data class LineItem(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val transactionId: String,
    val pluCode: String,
    val name: String,
    val quantity: Double,
    val unitPrice: Double,
    val taxAmount: Double,
    val total: Double
)
