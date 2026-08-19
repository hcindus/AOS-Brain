package com.ps.pos.viewmodel;

@kotlin.Metadata(mv = {1, 9, 0}, k = 1, xi = 48, d1 = {"\u0000N\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\u0010\u0006\n\u0002\b\u0002\n\u0002\u0010 \n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\b\r\n\u0002\u0010\u0002\n\u0002\b\u0003\n\u0002\u0010\u0007\n\u0000\n\u0002\u0010\b\n\u0002\b\u0005\u0018\u00002\u00020\u0001:\u0001(B\u0005\u00a2\u0006\u0002\u0010\u0002J\u0006\u0010\u001d\u001a\u00020\u001eJ\b\u0010\u001f\u001a\u00020\u001eH\u0002J\u0006\u0010 \u001a\u00020\u0005J\u0006\u0010!\u001a\u00020\"J\u0006\u0010#\u001a\u00020$J\b\u0010%\u001a\u00020\u001eH\u0002J\u000e\u0010&\u001a\u00020\u001e2\u0006\u0010\'\u001a\u00020\u000bR\u0014\u0010\u0003\u001a\b\u0012\u0004\u0012\u00020\u00050\u0004X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u0014\u0010\u0006\u001a\b\u0012\u0004\u0012\u00020\u00050\u0004X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u001a\u0010\u0007\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\t0\b0\u0004X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u0014\u0010\n\u001a\b\u0012\u0004\u0012\u00020\u000b0\u0004X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u001a\u0010\f\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\r0\b0\u0004X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u0014\u0010\u000e\u001a\b\u0012\u0004\u0012\u00020\u00050\u0004X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u0017\u0010\u000f\u001a\b\u0012\u0004\u0012\u00020\u00050\u0010\u00a2\u0006\b\n\u0000\u001a\u0004\b\u0011\u0010\u0012R\u0017\u0010\u0013\u001a\b\u0012\u0004\u0012\u00020\u00050\u0010\u00a2\u0006\b\n\u0000\u001a\u0004\b\u0014\u0010\u0012R\u001d\u0010\u0015\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\t0\b0\u0010\u00a2\u0006\b\n\u0000\u001a\u0004\b\u0016\u0010\u0012R\u0017\u0010\u0017\u001a\b\u0012\u0004\u0012\u00020\u000b0\u0010\u00a2\u0006\b\n\u0000\u001a\u0004\b\u0018\u0010\u0012R\u001d\u0010\u0019\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\r0\b0\u0010\u00a2\u0006\b\n\u0000\u001a\u0004\b\u001a\u0010\u0012R\u0017\u0010\u001b\u001a\b\u0012\u0004\u0012\u00020\u00050\u0010\u00a2\u0006\b\n\u0000\u001a\u0004\b\u001c\u0010\u0012\u00a8\u0006)"}, d2 = {"Lcom/ps/pos/viewmodel/ReportsViewModel;", "Landroidx/lifecycle/ViewModel;", "()V", "_dailySales", "Lkotlinx/coroutines/flow/MutableStateFlow;", "", "_monthlySales", "_salesByCategory", "", "Lcom/ps/pos/viewmodel/CategorySales;", "_selectedPeriod", "Lcom/ps/pos/viewmodel/ReportsViewModel$TimePeriod;", "_topProducts", "Lcom/ps/pos/viewmodel/TopProduct;", "_weeklySales", "dailySales", "Lkotlinx/coroutines/flow/StateFlow;", "getDailySales", "()Lkotlinx/coroutines/flow/StateFlow;", "monthlySales", "getMonthlySales", "salesByCategory", "getSalesByCategory", "selectedPeriod", "getSelectedPeriod", "topProducts", "getTopProducts", "weeklySales", "getWeeklySales", "exportReport", "", "generateMockData", "getAverageTransaction", "getSalesTrend", "", "getTransactionCount", "", "loadReports", "onPeriodSelected", "period", "TimePeriod", "app_debug"})
public final class ReportsViewModel extends androidx.lifecycle.ViewModel {
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.MutableStateFlow<com.ps.pos.viewmodel.ReportsViewModel.TimePeriod> _selectedPeriod = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.StateFlow<com.ps.pos.viewmodel.ReportsViewModel.TimePeriod> selectedPeriod = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.MutableStateFlow<java.lang.Double> _dailySales = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.StateFlow<java.lang.Double> dailySales = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.MutableStateFlow<java.lang.Double> _weeklySales = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.StateFlow<java.lang.Double> weeklySales = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.MutableStateFlow<java.lang.Double> _monthlySales = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.StateFlow<java.lang.Double> monthlySales = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.MutableStateFlow<java.util.List<com.ps.pos.viewmodel.TopProduct>> _topProducts = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.StateFlow<java.util.List<com.ps.pos.viewmodel.TopProduct>> topProducts = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.MutableStateFlow<java.util.List<com.ps.pos.viewmodel.CategorySales>> _salesByCategory = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.StateFlow<java.util.List<com.ps.pos.viewmodel.CategorySales>> salesByCategory = null;
    
    public ReportsViewModel() {
        super();
    }
    
    @org.jetbrains.annotations.NotNull
    public final kotlinx.coroutines.flow.StateFlow<com.ps.pos.viewmodel.ReportsViewModel.TimePeriod> getSelectedPeriod() {
        return null;
    }
    
    @org.jetbrains.annotations.NotNull
    public final kotlinx.coroutines.flow.StateFlow<java.lang.Double> getDailySales() {
        return null;
    }
    
    @org.jetbrains.annotations.NotNull
    public final kotlinx.coroutines.flow.StateFlow<java.lang.Double> getWeeklySales() {
        return null;
    }
    
    @org.jetbrains.annotations.NotNull
    public final kotlinx.coroutines.flow.StateFlow<java.lang.Double> getMonthlySales() {
        return null;
    }
    
    @org.jetbrains.annotations.NotNull
    public final kotlinx.coroutines.flow.StateFlow<java.util.List<com.ps.pos.viewmodel.TopProduct>> getTopProducts() {
        return null;
    }
    
    @org.jetbrains.annotations.NotNull
    public final kotlinx.coroutines.flow.StateFlow<java.util.List<com.ps.pos.viewmodel.CategorySales>> getSalesByCategory() {
        return null;
    }
    
    private final void loadReports() {
    }
    
    private final void generateMockData() {
    }
    
    public final void onPeriodSelected(@org.jetbrains.annotations.NotNull
    com.ps.pos.viewmodel.ReportsViewModel.TimePeriod period) {
    }
    
    public final void exportReport() {
    }
    
    public final float getSalesTrend() {
        return 0.0F;
    }
    
    public final double getAverageTransaction() {
        return 0.0;
    }
    
    public final int getTransactionCount() {
        return 0;
    }
    
    @kotlin.Metadata(mv = {1, 9, 0}, k = 1, xi = 48, d1 = {"\u0000\f\n\u0002\u0018\u0002\n\u0002\u0010\u0010\n\u0002\b\u0006\b\u0086\u0081\u0002\u0018\u00002\b\u0012\u0004\u0012\u00020\u00000\u0001B\u0007\b\u0002\u00a2\u0006\u0002\u0010\u0002j\u0002\b\u0003j\u0002\b\u0004j\u0002\b\u0005j\u0002\b\u0006\u00a8\u0006\u0007"}, d2 = {"Lcom/ps/pos/viewmodel/ReportsViewModel$TimePeriod;", "", "(Ljava/lang/String;I)V", "TODAY", "WEEK", "MONTH", "YEAR", "app_debug"})
    public static enum TimePeriod {
        /*public static final*/ TODAY /* = new TODAY() */,
        /*public static final*/ WEEK /* = new WEEK() */,
        /*public static final*/ MONTH /* = new MONTH() */,
        /*public static final*/ YEAR /* = new YEAR() */;
        
        TimePeriod() {
        }
        
        @org.jetbrains.annotations.NotNull
        public static kotlin.enums.EnumEntries<com.ps.pos.viewmodel.ReportsViewModel.TimePeriod> getEntries() {
            return null;
        }
    }
}