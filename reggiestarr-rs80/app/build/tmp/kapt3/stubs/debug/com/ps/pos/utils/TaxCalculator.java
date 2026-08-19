package com.ps.pos.utils;

@kotlin.Metadata(mv = {1, 9, 0}, k = 1, xi = 48, d1 = {"\u0000\u0014\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0002\b\u0002\n\u0002\u0010\u0006\n\u0002\b\u0004\b\u00c6\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002\u00a2\u0006\u0002\u0010\u0002J\u000e\u0010\u0005\u001a\u00020\u00042\u0006\u0010\u0006\u001a\u00020\u0004J\u000e\u0010\u0007\u001a\u00020\u00042\u0006\u0010\u0006\u001a\u00020\u0004R\u000e\u0010\u0003\u001a\u00020\u0004X\u0082T\u00a2\u0006\u0002\n\u0000\u00a8\u0006\b"}, d2 = {"Lcom/ps/pos/utils/TaxCalculator;", "", "()V", "TAX_RATE", "", "calculateTax", "subtotal", "calculateTotal", "app_debug"})
public final class TaxCalculator {
    private static final double TAX_RATE = 0.0825;
    @org.jetbrains.annotations.NotNull
    public static final com.ps.pos.utils.TaxCalculator INSTANCE = null;
    
    private TaxCalculator() {
        super();
    }
    
    public final double calculateTax(double subtotal) {
        return 0.0;
    }
    
    public final double calculateTotal(double subtotal) {
        return 0.0;
    }
}