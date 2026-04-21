package com.ps.pos.data

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import com.ps.pos.data.dao.LineItemDao
import com.ps.pos.data.dao.ProductDao
import com.ps.pos.data.dao.TransactionDao
import com.ps.pos.data.entities.LineItem
import com.ps.pos.data.entities.Product
import com.ps.pos.data.entities.Transaction

@Database(
    entities = [Product::class, Transaction::class, LineItem::class],
    version = 1,
    exportSchema = false
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun productDao(): ProductDao
    abstract fun transactionDao(): TransactionDao
    abstract fun lineItemDao(): LineItemDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getDatabase(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "reggiestarr_db"
                )
                    .fallbackToDestructiveMigration()
                    .build()
                INSTANCE = instance
                instance
            }
        }
    }
}
