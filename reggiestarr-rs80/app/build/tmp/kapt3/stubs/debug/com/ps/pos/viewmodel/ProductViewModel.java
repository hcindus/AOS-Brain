package com.ps.pos.viewmodel;

@kotlin.Metadata(mv = {1, 9, 0}, k = 1, xi = 48, d1 = {"\u00006\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\u0010 \n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u000e\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0005\n\u0002\u0010\u0002\n\u0002\b\u000b\u0018\u00002\u00020\u0001B\u000f\u0012\b\b\u0002\u0010\u0002\u001a\u00020\u0003\u00a2\u0006\u0002\u0010\u0004J\u000e\u0010\u0011\u001a\u00020\u00122\u0006\u0010\u0013\u001a\u00020\bJ\u000e\u0010\u0014\u001a\u00020\u00122\u0006\u0010\u0013\u001a\u00020\bJ\u000e\u0010\u0015\u001a\b\u0012\u0004\u0012\u00020\b0\u0007H\u0002J\u000e\u0010\u0016\u001a\u00020\u0012H\u0082@\u00a2\u0006\u0002\u0010\u0017J\u000e\u0010\u0018\u001a\u00020\u00122\u0006\u0010\u0019\u001a\u00020\nJ\u0016\u0010\u001a\u001a\u00020\u00122\u0006\u0010\u0019\u001a\u00020\nH\u0082@\u00a2\u0006\u0002\u0010\u001bJ\u000e\u0010\u001c\u001a\u00020\u00122\u0006\u0010\u0013\u001a\u00020\bR\u001a\u0010\u0005\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\b0\u00070\u0006X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u0014\u0010\t\u001a\b\u0012\u0004\u0012\u00020\n0\u0006X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u001d\u0010\u000b\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\b0\u00070\f\u00a2\u0006\b\n\u0000\u001a\u0004\b\r\u0010\u000eR\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u0017\u0010\u000f\u001a\b\u0012\u0004\u0012\u00020\n0\f\u00a2\u0006\b\n\u0000\u001a\u0004\b\u0010\u0010\u000e\u00a8\u0006\u001d"}, d2 = {"Lcom/ps/pos/viewmodel/ProductViewModel;", "Landroidx/lifecycle/ViewModel;", "repository", "Lcom/ps/pos/POSRepository;", "(Lcom/ps/pos/POSRepository;)V", "_products", "Lkotlinx/coroutines/flow/MutableStateFlow;", "", "Lcom/ps/pos/data/entities/Product;", "_searchQuery", "", "products", "Lkotlinx/coroutines/flow/StateFlow;", "getProducts", "()Lkotlinx/coroutines/flow/StateFlow;", "searchQuery", "getSearchQuery", "addProduct", "", "product", "deleteProduct", "getMockProducts", "loadProducts", "(Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "onSearchQueryChange", "query", "searchProducts", "(Ljava/lang/String;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "updateProduct", "app_debug"})
public final class ProductViewModel extends androidx.lifecycle.ViewModel {
    @org.jetbrains.annotations.NotNull
    private final com.ps.pos.POSRepository repository = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.MutableStateFlow<java.lang.String> _searchQuery = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.StateFlow<java.lang.String> searchQuery = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.MutableStateFlow<java.util.List<com.ps.pos.data.entities.Product>> _products = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.StateFlow<java.util.List<com.ps.pos.data.entities.Product>> products = null;
    
    public ProductViewModel(@org.jetbrains.annotations.NotNull
    com.ps.pos.POSRepository repository) {
        super();
    }
    
    @org.jetbrains.annotations.NotNull
    public final kotlinx.coroutines.flow.StateFlow<java.lang.String> getSearchQuery() {
        return null;
    }
    
    @org.jetbrains.annotations.NotNull
    public final kotlinx.coroutines.flow.StateFlow<java.util.List<com.ps.pos.data.entities.Product>> getProducts() {
        return null;
    }
    
    private final java.lang.Object loadProducts(kotlin.coroutines.Continuation<? super kotlin.Unit> $completion) {
        return null;
    }
    
    private final java.lang.Object searchProducts(java.lang.String query, kotlin.coroutines.Continuation<? super kotlin.Unit> $completion) {
        return null;
    }
    
    private final java.util.List<com.ps.pos.data.entities.Product> getMockProducts() {
        return null;
    }
    
    public final void onSearchQueryChange(@org.jetbrains.annotations.NotNull
    java.lang.String query) {
    }
    
    public final void addProduct(@org.jetbrains.annotations.NotNull
    com.ps.pos.data.entities.Product product) {
    }
    
    public final void updateProduct(@org.jetbrains.annotations.NotNull
    com.ps.pos.data.entities.Product product) {
    }
    
    public final void deleteProduct(@org.jetbrains.annotations.NotNull
    com.ps.pos.data.entities.Product product) {
    }
    
    public ProductViewModel() {
        super();
    }
}