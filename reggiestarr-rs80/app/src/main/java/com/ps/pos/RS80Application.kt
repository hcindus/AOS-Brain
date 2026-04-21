package com.ps.pos

import android.app.Application
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import com.ps.pos.data.AppDatabase
import com.ps.pos.data.entities.Product

class RS80Application : Application() {
    
    val database by lazy { AppDatabase.getDatabase(this) }
    val repository by lazy { POSRepository() }
    
    override fun onCreate() {
        super.onCreate()
        // App initialization complete
    }
}
