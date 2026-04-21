package com.ps.pos.data.entities

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "products")
data class Product(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val plu: String,
    val name: String,
    val price: Double,
    val category: String,
    val barcode: String? = null,
    val cost: Double? = null,
    val stockQuantity: Double? = null,
    val isActive: Boolean = true
)