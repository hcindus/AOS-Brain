package com.ps.pos.viewmodel;

@kotlin.Metadata(mv = {1, 9, 0}, k = 1, xi = 48, d1 = {"\u0000T\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\u0010 \n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0006\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\b\n\u0002\b\u0007\n\u0002\u0010\u0002\n\u0002\b\u0005\n\u0002\u0010\u000e\n\u0002\b\f\u0018\u00002\u00020\u0001B\u000f\u0012\b\b\u0002\u0010\u0002\u001a\u00020\u0003\u00a2\u0006\u0002\u0010\u0004J\u000e\u0010\u001d\u001a\u00020\u001eH\u0082@\u00a2\u0006\u0002\u0010\u001fJ\u0006\u0010 \u001a\u00020\u001eJ\u0006\u0010!\u001a\u00020\u001eJ\u0016\u0010\"\u001a\u00020\u001e2\u0006\u0010#\u001a\u00020$2\u0006\u0010%\u001a\u00020\nJ\b\u0010&\u001a\u00020$H\u0002J\u000e\u0010\'\u001a\u00020\u001e2\u0006\u0010(\u001a\u00020$J\u000e\u0010)\u001a\u00020\u001e2\u0006\u0010*\u001a\u00020$J\u000e\u0010+\u001a\u00020\u001e2\u0006\u0010,\u001a\u00020\bJ\u000e\u0010-\u001a\u00020\u001e2\u0006\u0010.\u001a\u00020\u0016J\b\u0010/\u001a\u00020\u001eH\u0002R\u001a\u0010\u0005\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\b0\u00070\u0006X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u0014\u0010\t\u001a\b\u0012\u0004\u0012\u00020\n0\u0006X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u0014\u0010\u000b\u001a\b\u0012\u0004\u0012\u00020\n0\u0006X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u0014\u0010\f\u001a\b\u0012\u0004\u0012\u00020\n0\u0006X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u001a\u0010\r\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\u000e0\u00070\u0006X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u001d\u0010\u000f\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\b0\u00070\u0010\u00a2\u0006\b\n\u0000\u001a\u0004\b\u0011\u0010\u0012R\u0010\u0010\u0013\u001a\u0004\u0018\u00010\u0014X\u0082\u000e\u00a2\u0006\u0002\n\u0000R\u000e\u0010\u0015\u001a\u00020\u0016X\u0082\u000e\u00a2\u0006\u0002\n\u0000R\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u0017\u0010\u0017\u001a\b\u0012\u0004\u0012\u00020\n0\u0010\u00a2\u0006\b\n\u0000\u001a\u0004\b\u0018\u0010\u0012R\u0017\u0010\u0019\u001a\b\u0012\u0004\u0012\u00020\n0\u0010\u00a2\u0006\b\n\u0000\u001a\u0004\b\u001a\u0010\u0012R\u0017\u0010\u001b\u001a\b\u0012\u0004\u0012\u00020\n0\u0010\u00a2\u0006\b\n\u0000\u001a\u0004\b\u001c\u0010\u0012\u00a8\u00060"}, d2 = {"Lcom/ps/pos/viewmodel/RegisterViewModel;", "Landroidx/lifecycle/ViewModel;", "repository", "Lcom/ps/pos/POSRepository;", "(Lcom/ps/pos/POSRepository;)V", "_cartItems", "Lkotlinx/coroutines/flow/MutableStateFlow;", "", "Lcom/ps/pos/data/entities/LineItem;", "_subtotal", "", "_tax", "_total", "_transactions", "Lcom/ps/pos/data/entities/Transaction;", "cartItems", "Lkotlinx/coroutines/flow/StateFlow;", "getCartItems", "()Lkotlinx/coroutines/flow/StateFlow;", "currentProduct", "Lcom/ps/pos/data/entities/Product;", "currentQuantity", "", "subtotal", "getSubtotal", "tax", "getTax", "total", "getTotal", "addSampleProducts", "", "(Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "addToCart", "clearCart", "completeTransaction", "paymentType", "", "tendered", "generateTransactionNumber", "lookupProduct", "plu", "lookupProductByBarcode", "barcode", "removeFromCart", "item", "setQuantity", "qty", "updateTotals", "app_debug"})
public final class RegisterViewModel extends androidx.lifecycle.ViewModel {
    @org.jetbrains.annotations.NotNull
    private final com.ps.pos.POSRepository repository = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.MutableStateFlow<java.util.List<com.ps.pos.data.entities.LineItem>> _cartItems = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.StateFlow<java.util.List<com.ps.pos.data.entities.LineItem>> cartItems = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.MutableStateFlow<java.lang.Double> _subtotal = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.StateFlow<java.lang.Double> subtotal = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.MutableStateFlow<java.lang.Double> _tax = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.StateFlow<java.lang.Double> tax = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.MutableStateFlow<java.lang.Double> _total = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.StateFlow<java.lang.Double> total = null;
    @org.jetbrains.annotations.Nullable
    private com.ps.pos.data.entities.Product currentProduct;
    private int currentQuantity = 1;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.MutableStateFlow<java.util.List<com.ps.pos.data.entities.Transaction>> _transactions = null;
    
    public RegisterViewModel(@org.jetbrains.annotations.NotNull
    com.ps.pos.POSRepository repository) {
        super();
    }
    
    @org.jetbrains.annotations.NotNull
    public final kotlinx.coroutines.flow.StateFlow<java.util.List<com.ps.pos.data.entities.LineItem>> getCartItems() {
        return null;
    }
    
    @org.jetbrains.annotations.NotNull
    public final kotlinx.coroutines.flow.StateFlow<java.lang.Double> getSubtotal() {
        return null;
    }
    
    @org.jetbrains.annotations.NotNull
    public final kotlinx.coroutines.flow.StateFlow<java.lang.Double> getTax() {
        return null;
    }
    
    @org.jetbrains.annotations.NotNull
    public final kotlinx.coroutines.flow.StateFlow<java.lang.Double> getTotal() {
        return null;
    }
    
    private final java.lang.Object addSampleProducts(kotlin.coroutines.Continuation<? super kotlin.Unit> $completion) {
        return null;
    }
    
    public final void lookupProduct(@org.jetbrains.annotations.NotNull
    java.lang.String plu) {
    }
    
    public final void lookupProductByBarcode(@org.jetbrains.annotations.NotNull
    java.lang.String barcode) {
    }
    
    public final void setQuantity(int qty) {
    }
    
    public final void addToCart() {
    }
    
    public final void removeFromCart(@org.jetbrains.annotations.NotNull
    com.ps.pos.data.entities.LineItem item) {
    }
    
    public final void clearCart() {
    }
    
    private final void updateTotals() {
    }
    
    public final void completeTransaction(@org.jetbrains.annotations.NotNull
    java.lang.String paymentType, double tendered) {
    }
    
    private final java.lang.String generateTransactionNumber() {
        return null;
    }
    
    public RegisterViewModel() {
        super();
    }
}