package com.ps.pos.data.dao

import androidx.room.*
import com.ps.pos.data.entities.Product
import kotlinx.coroutines.flow.Flow

@Dao
interface ProductDao {
    @Query("SELECT * FROM products ORDER BY name")
    fun getAll(): Flow<List<Product>>

    @Query("SELECT * FROM products WHERE department = :dept ORDER BY name")
    fun getByDepartment(dept: String): Flow<List<Product>>

    @Query("SELECT * FROM products WHERE pluCode = :code LIMIT 1")
    suspend fun getByPlu(code: String): Product?

    @Query("SELECT * FROM products WHERE openPrice = 0 ORDER BY name")
    fun getFixedPrice(): Flow<List<Product>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(product: Product)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(products: List<Product>)

    @Delete
    suspend fun delete(product: Product)

    @Query("UPDATE products SET stock = stock - :qty WHERE pluCode = :code AND trackInventory = 1")
    suspend fun decrementStock(code: String, qty: Double)
}
