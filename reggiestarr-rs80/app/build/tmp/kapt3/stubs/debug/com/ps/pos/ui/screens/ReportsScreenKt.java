package com.ps.pos.ui.screens;

@kotlin.Metadata(mv = {1, 9, 0}, k = 2, xi = 48, d1 = {"\u0000H\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0010\u000e\n\u0000\n\u0002\u0010\u0006\n\u0000\n\u0002\u0010\u0007\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\b\n\u0002\b\u0004\u001a \u0010\u0000\u001a\u00020\u00012\u0006\u0010\u0002\u001a\u00020\u00032\u0006\u0010\u0004\u001a\u00020\u00052\u0006\u0010\u0006\u001a\u00020\u0007H\u0007\u001a$\u0010\b\u001a\u00020\u00012\u0006\u0010\t\u001a\u00020\n2\u0012\u0010\u000b\u001a\u000e\u0012\u0004\u0012\u00020\n\u0012\u0004\u0012\u00020\u00010\fH\u0007\u001a \u0010\r\u001a\u00020\u00012\f\u0010\u000e\u001a\b\u0012\u0004\u0012\u00020\u00010\u000f2\b\b\u0002\u0010\u0010\u001a\u00020\u0011H\u0007\u001a\"\u0010\u0012\u001a\u00020\u00012\u0006\u0010\u0013\u001a\u00020\u00032\u0006\u0010\u0004\u001a\u00020\u00052\b\b\u0002\u0010\u0014\u001a\u00020\u0015H\u0007\u001a(\u0010\u0016\u001a\u00020\u00012\u0006\u0010\u0017\u001a\u00020\u00182\u0006\u0010\u0019\u001a\u00020\u00032\u0006\u0010\u001a\u001a\u00020\u00182\u0006\u0010\u001b\u001a\u00020\u0005H\u0007\u00a8\u0006\u001c"}, d2 = {"CategorySalesRow", "", "category", "", "amount", "", "percentage", "", "PeriodSelector", "selectedPeriod", "Lcom/ps/pos/viewmodel/ReportsViewModel$TimePeriod;", "onPeriodSelected", "Lkotlin/Function1;", "ReportsScreen", "onBack", "Lkotlin/Function0;", "viewModel", "Lcom/ps/pos/viewmodel/ReportsViewModel;", "SummaryCard", "title", "modifier", "Landroidx/compose/ui/Modifier;", "TopProductRow", "rank", "", "name", "quantity", "revenue", "app_debug"})
@kotlin.OptIn(markerClass = {androidx.compose.material3.ExperimentalMaterial3Api.class})
public final class ReportsScreenKt {
    
    @kotlin.OptIn(markerClass = {androidx.compose.material3.ExperimentalMaterial3Api.class})
    @androidx.compose.runtime.Composable
    public static final void ReportsScreen(@org.jetbrains.annotations.NotNull
    kotlin.jvm.functions.Function0<kotlin.Unit> onBack, @org.jetbrains.annotations.NotNull
    com.ps.pos.viewmodel.ReportsViewModel viewModel) {
    }
    
    @androidx.compose.runtime.Composable
    public static final void PeriodSelector(@org.jetbrains.annotations.NotNull
    com.ps.pos.viewmodel.ReportsViewModel.TimePeriod selectedPeriod, @org.jetbrains.annotations.NotNull
    kotlin.jvm.functions.Function1<? super com.ps.pos.viewmodel.ReportsViewModel.TimePeriod, kotlin.Unit> onPeriodSelected) {
    }
    
    @androidx.compose.runtime.Composable
    public static final void SummaryCard(@org.jetbrains.annotations.NotNull
    java.lang.String title, double amount, @org.jetbrains.annotations.NotNull
    androidx.compose.ui.Modifier modifier) {
    }
    
    @androidx.compose.runtime.Composable
    public static final void TopProductRow(int rank, @org.jetbrains.annotations.NotNull
    java.lang.String name, int quantity, double revenue) {
    }
    
    @androidx.compose.runtime.Composable
    public static final void CategorySalesRow(@org.jetbrains.annotations.NotNull
    java.lang.String category, double amount, float percentage) {
    }
}