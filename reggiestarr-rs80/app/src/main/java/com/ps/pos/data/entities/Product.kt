package com.ps.pos.data.entities

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "products")
data class Product(
    @PrimaryKey val pluCode: String,
    val name: String,
    val price: Double,
    val department: String = "General",
    val taxRate: Double = 0.0,
    val taxType: String = "EXCLUSIVE", // EXCLUSIVE, INCLUSIVE, EXEMPT
    val openPrice: Boolean = false,    // If true, price can be overridden at sale
    val stock: Int = 0,
    val trackInventory: Boolean = false
)
