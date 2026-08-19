package com.ps.pos.data.dao;

@kotlin.Metadata(mv = {1, 9, 0}, k = 1, xi = 48, d1 = {"\u00004\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\u0010 \n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0002\b\u0004\n\u0002\u0010\t\n\u0002\b\u0004\bg\u0018\u00002\u00020\u0001J\u0016\u0010\u0002\u001a\u00020\u00032\u0006\u0010\u0004\u001a\u00020\u0005H\u00a7@\u00a2\u0006\u0002\u0010\u0006J\u0014\u0010\u0007\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\u00050\t0\bH\'J\u0018\u0010\n\u001a\u0004\u0018\u00010\u00052\u0006\u0010\u000b\u001a\u00020\fH\u00a7@\u00a2\u0006\u0002\u0010\rJ\u0018\u0010\u000e\u001a\u0004\u0018\u00010\u00052\u0006\u0010\u000f\u001a\u00020\fH\u00a7@\u00a2\u0006\u0002\u0010\rJ\u0016\u0010\u0010\u001a\u00020\u00112\u0006\u0010\u0004\u001a\u00020\u0005H\u00a7@\u00a2\u0006\u0002\u0010\u0006J\u001c\u0010\u0012\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\u00050\t0\b2\u0006\u0010\u0013\u001a\u00020\fH\'J\u0016\u0010\u0014\u001a\u00020\u00032\u0006\u0010\u0004\u001a\u00020\u0005H\u00a7@\u00a2\u0006\u0002\u0010\u0006\u00a8\u0006\u0015"}, d2 = {"Lcom/ps/pos/data/dao/ProductDao;", "", "delete", "", "product", "Lcom/ps/pos/data/entities/Product;", "(Lcom/ps/pos/data/entities/Product;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "getAllProducts", "Lkotlinx/coroutines/flow/Flow;", "", "getByBarcode", "barcode", "", "(Ljava/lang/String;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "getByPlu", "plu", "insert", "", "searchProducts", "query", "update", "app_debug"})
@androidx.room.Dao
public abstract interface ProductDao {
    
    @androidx.room.Query(value = "SELECT * FROM products WHERE isActive = 1 ORDER BY name")
    @org.jetbrains.annotations.NotNull
    public abstract kotlinx.coroutines.flow.Flow<java.util.List<com.ps.pos.data.entities.Product>> getAllProducts();
    
    @androidx.room.Query(value = "SELECT * FROM products WHERE plu = :plu LIMIT 1")
    @org.jetbrains.annotations.Nullable
    public abstract java.lang.Object getByPlu(@org.jetbrains.annotations.NotNull
    java.lang.String plu, @org.jetbrains.annotations.NotNull
    kotlin.coroutines.Continuation<? super com.ps.pos.data.entities.Product> $completion);
    
    @androidx.room.Query(value = "SELECT * FROM products WHERE barcode = :barcode LIMIT 1")
    @org.jetbrains.annotations.Nullable
    public abstract java.lang.Object getByBarcode(@org.jetbrains.annotations.NotNull
    java.lang.String barcode, @org.jetbrains.annotations.NotNull
    kotlin.coroutines.Continuation<? super com.ps.pos.data.entities.Product> $completion);
    
    @androidx.room.Query(value = "SELECT * FROM products WHERE name LIKE \'%\' || :query || \'%\'")
    @org.jetbrains.annotations.NotNull
    public abstract kotlinx.coroutines.flow.Flow<java.util.List<com.ps.pos.data.entities.Product>> searchProducts(@org.jetbrains.annotations.NotNull
    java.lang.String query);
    
    @androidx.room.Insert(onConflict = 1)
    @org.jetbrains.annotations.Nullable
    public abstract java.lang.Object insert(@org.jetbrains.annotations.NotNull
    com.ps.pos.data.entities.Product product, @org.jetbrains.annotations.NotNull
    kotlin.coroutines.Continuation<? super java.lang.Long> $completion);
    
    @androidx.room.Update
    @org.jetbrains.annotations.Nullable
    public abstract java.lang.Object update(@org.jetbrains.annotations.NotNull
    com.ps.pos.data.entities.Product product, @org.jetbrains.annotations.NotNull
    kotlin.coroutines.Continuation<? super kotlin.Unit> $completion);
    
    @androidx.room.Delete
    @org.jetbrains.annotations.Nullable
    public abstract java.lang.Object delete(@org.jetbrains.annotations.NotNull
    com.ps.pos.data.entities.Product product, @org.jetbrains.annotations.NotNull
    kotlin.coroutines.Continuation<? super kotlin.Unit> $completion);
}