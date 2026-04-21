package com.ps.pos

import android.app.Application
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import com.ps.pos.data.AppDatabase
import com.ps.pos.data.entities.Product

class RS80Application : Application() {
    
    val database by lazy { AppDatabase.getDatabase(this) }
    val repository by lazy { POSRepository(database) }
    
    override fun onCreate() {
        super.onCreate()
        
        // Seed sample data on first launch
        CoroutineScope(Dispatchers.IO).launch {
            seedSampleData()
        }
    }
    
    private suspend fun seedSampleData() {
        val productDao = database.productDao()
        
        // Check if already seeded
        val existing = productDao.getByPlu("BURGER")
        if (existing != null) return
        
        // Sample products
        val sampleProducts = listOf(
            Product(
                pluCode = "BURGER",
                name = "Cheeseburger",
                price = 8.99,
                department = "Food",
                taxRate = 0.0875,
                taxType = "EXCLUSIVE",
                stock = 100,
                trackInventory = true
            ),
            Product(
                pluCode = "FRIES",
                name = "French Fries",
                price = 3.99,
                department = "Food", 
                taxRate = 0.0875,
                taxType = "EXCLUSIVE",
                stock = 100,
                trackInventory = true
            ),
            Product(
                pluCode = "SODA",
                name = "Soda",
                price = 2.50,
                department = "Drinks",
                taxRate = 0.0875,
                taxType = "EXCLUSIVE",
                stock = 50,
                trackInventory = true
            ),
            Product(
                pluCode = "OPEN",
                name = "Open Price Item",
                price = 0.0,
                department = "Misc",
                taxRate = 0.0875,
                taxType = "EXCLUSIVE",
                openPrice = true,
                stock = 0,
                trackInventory = false
            ),
            Product(
                pluCode = "TAXINC",
                name = "Tax Inclusive Item",
                price = 10.00,
                department = "Food",
                taxRate = 0.0875,
                taxType = "INCLUSIVE",
                stock = 0,
                trackInventory = false
            ),
            Product(
                pluCode = "TAXEX",
                name = "Tax Exempt Item",
                price = 5.00,
                department = "Misc",
                taxRate = 0.0,
                taxType = "EXEMPT",
                stock = 0,
                trackInventory = false
            )
        )
        
        productDao.insertAll(sampleProducts)
    }
}
