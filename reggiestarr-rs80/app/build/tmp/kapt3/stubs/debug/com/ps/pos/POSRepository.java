package com.ps.pos;

@kotlin.Metadata(mv = {1, 9, 0}, k = 1, xi = 48, d1 = {"\u0000<\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0002\b\u0002\n\u0002\u0010!\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0002\b\u0002\n\u0002\u0010\u0002\n\u0002\b\u0005\n\u0002\u0010 \n\u0002\b\u0002\u0018\u00002\u00020\u0001B\u0005\u00a2\u0006\u0002\u0010\u0002J\u0018\u0010\n\u001a\u0004\u0018\u00010\u00072\u0006\u0010\u000b\u001a\u00020\fH\u0086@\u00a2\u0006\u0002\u0010\rJ\u0016\u0010\u000e\u001a\u00020\u000f2\u0006\u0010\u0010\u001a\u00020\u0007H\u0086@\u00a2\u0006\u0002\u0010\u0011J$\u0010\u0012\u001a\u00020\u000f2\u0006\u0010\u0013\u001a\u00020\t2\f\u0010\u0014\u001a\b\u0012\u0004\u0012\u00020\u00050\u0015H\u0086@\u00a2\u0006\u0002\u0010\u0016R\u0014\u0010\u0003\u001a\b\u0012\u0004\u0012\u00020\u00050\u0004X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u0014\u0010\u0006\u001a\b\u0012\u0004\u0012\u00020\u00070\u0004X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u0014\u0010\b\u001a\b\u0012\u0004\u0012\u00020\t0\u0004X\u0082\u0004\u00a2\u0006\u0002\n\u0000\u00a8\u0006\u0017"}, d2 = {"Lcom/ps/pos/POSRepository;", "", "()V", "lineItems", "", "Lcom/ps/pos/data/entities/LineItem;", "products", "Lcom/ps/pos/data/entities/Product;", "transactions", "Lcom/ps/pos/data/entities/Transaction;", "getProductByPlu", "plu", "", "(Ljava/lang/String;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "insertProduct", "", "product", "(Lcom/ps/pos/data/entities/Product;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "insertTransaction", "transaction", "items", "", "(Lcom/ps/pos/data/entities/Transaction;Ljava/util/List;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "app_debug"})
public final class POSRepository {
    @org.jetbrains.annotations.NotNull
    private final java.util.List<com.ps.pos.data.entities.Product> products = null;
    @org.jetbrains.annotations.NotNull
    private final java.util.List<com.ps.pos.data.entities.Transaction> transactions = null;
    @org.jetbrains.annotations.NotNull
    private final java.util.List<com.ps.pos.data.entities.LineItem> lineItems = null;
    
    public POSRepository() {
        super();
    }
    
    @org.jetbrains.annotations.Nullable
    public final java.lang.Object getProductByPlu(@org.jetbrains.annotations.NotNull
    java.lang.String plu, @org.jetbrains.annotations.NotNull
    kotlin.coroutines.Continuation<? super com.ps.pos.data.entities.Product> $completion) {
        return null;
    }
    
    @org.jetbrains.annotations.Nullable
    public final java.lang.Object insertProduct(@org.jetbrains.annotations.NotNull
    com.ps.pos.data.entities.Product product, @org.jetbrains.annotations.NotNull
    kotlin.coroutines.Continuation<? super kotlin.Unit> $completion) {
        return null;
    }
    
    @org.jetbrains.annotations.Nullable
    public final java.lang.Object insertTransaction(@org.jetbrains.annotations.NotNull
    com.ps.pos.data.entities.Transaction transaction, @org.jetbrains.annotations.NotNull
    java.util.List<com.ps.pos.data.entities.LineItem> items, @org.jetbrains.annotations.NotNull
    kotlin.coroutines.Continuation<? super kotlin.Unit> $completion) {
        return null;
    }
}