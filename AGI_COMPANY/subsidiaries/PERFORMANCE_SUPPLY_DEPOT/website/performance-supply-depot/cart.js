/**
 * SHOPPING CART SYSTEM
 * Fully interactive cart with localStorage persistence
 */

class ShoppingCart {
    constructor() {
        this.items = this.loadCart();
        this.updateCartUI();
    }

    loadCart() {
        const saved = localStorage.getItem('agi_cart');
        return saved ? JSON.parse(saved) : [];
    }

    saveCart() {
        localStorage.setItem('agi_cart', JSON.stringify(this.items));
        this.updateCartUI();
    }

    addItem(product) {
        const existing = this.items.find(item => item.id === product.id);
        
        if (existing) {
            existing.quantity += 1;
        } else {
            this.items.push({
                id: product.id,
                name: product.name,
                price: product.price,
                priceCents: product.priceCents,
                image: product.image,
                quantity: 1
            });
        }
        
        this.saveCart();
        this.showNotification(`${product.name} added to cart`);
    }

    removeItem(productId) {
        this.items = this.items.filter(item => item.id !== productId);
        this.saveCart();
    }

    updateQuantity(productId, quantity) {
        const item = this.items.find(item => item.id === productId);
        if (item) {
            item.quantity = Math.max(1, parseInt(quantity));
            this.saveCart();
        }
    }

    getTotal() {
        return this.items.reduce((sum, item) => sum + (item.priceCents * item.quantity), 0);
    }

    getTotalFormatted() {
        return (this.getTotal() / 100).toFixed(2);
    }

    getItemCount() {
        return this.items.reduce((sum, item) => sum + item.quantity, 0);
    }

    clearCart() {
        this.items = [];
        this.saveCart();
    }

    updateCartUI() {
        // Update cart icon count
        const cartCountElements = document.querySelectorAll('.cart-count');
        cartCountElements.forEach(el => {
            el.textContent = this.getItemCount();
            el.style.display = this.getItemCount() > 0 ? 'inline' : 'none';
        });

        // Update cart total
        const cartTotalElements = document.querySelectorAll('.cart-total');
        cartTotalElements.forEach(el => {
            el.textContent = `$${this.getTotalFormatted()}`;
        });
    }

    showNotification(message) {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            background: #22c55e;
            color: white;
            padding: 15px 25px;
            border-radius: 8px;
            font-weight: 600;
            z-index: 10000;
            animation: slideIn 0.3s ease;
        `;
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    renderCartPage() {
        const container = document.getElementById('cart-items');
        if (!container) return;

        if (this.items.length === 0) {
            container.innerHTML = `
                <div style="text-align: center; padding: 60px 20px;">
                    <h3 style="color: var(--primary); margin-bottom: 15px;">Your cart is empty</h3>
                    <p style="color: var(--text-light); margin-bottom: 25px;">Add some AGI agents to get started!</p>
                    <a href="index.html#products" class="btn">Browse Products</a>
                </div>
            `;
            return;
        }

        let html = `
            <div style="margin-bottom: 30px;">
                <h2 style="color: var(--primary); margin-bottom: 20px;">Cart Items (${this.getItemCount()})</h2>
        `;

        this.items.forEach(item => {
            html += `
                <div style="display: flex; align-items: center; padding: 20px; background: var(--bg-light); border-radius: 8px; margin-bottom: 15px;">
                    <div style="flex: 1;">
                        <h4 style="color: var(--primary); margin: 0 0 5px 0;">${item.name}</h4>
                        <p style="color: var(--text-light); margin: 0;">$${(item.priceCents / 100).toFixed(2)}/month</p>
                    </div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <button onclick="cart.updateQuantity('${item.id}', ${item.quantity - 1})" style="width: 32px; height: 32px; border: 1px solid var(--bg-dark); background: white; border-radius: 4px; cursor: pointer;">-</button>
                        <span style="font-weight: 600; min-width: 30px; text-align: center;">${item.quantity}</span>
                        <button onclick="cart.updateQuantity('${item.id}', ${item.quantity + 1})" style="width: 32px; height: 32px; border: 1px solid var(--bg-dark); background: white; border-radius: 4px; cursor: pointer;">+</button>
                    </div>
                    <div style="min-width: 100px; text-align: right; margin-left: 20px;">
                        <p style="font-weight: 700; color: var(--primary); margin: 0;">$${((item.priceCents * item.quantity) / 100).toFixed(2)}</p>
                        <button onclick="cart.removeItem('${item.id}')" style="background: none; border: none; color: #e53e3e; cursor: pointer; font-size: 12px; margin-top: 5px;">Remove</button>
                    </div>
                </div>
            `;
        });

        html += '</div>';

        // Summary
        html += `
            <div style="background: var(--primary); color: white; padding: 25px; border-radius: 8px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                    <span>Subtotal</span>
                    <span>$${this.getTotalFormatted()}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                    <span>Tax (0%)</span>
                    <span>$0.00</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 20px; font-weight: 700; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 15px;">
                    <span>Total</span>
                    <span>$${this.getTotalFormatted()}/mo</span>
                </div>
            </div>
        `;

        container.innerHTML = html;
    }
}

// Initialize cart
const cart = new ShoppingCart();

// Product catalog
const products = [
    { id: 'clerk', name: 'Clerk', price: '99.00', priceCents: 9900, image: '👨‍💼', description: 'Entry-level admin support' },
    { id: 'greet', name: 'Greet', price: '249.00', priceCents: 24900, image: '👋', description: '24/7 virtual receptionist' },
    { id: 'ledger', name: 'Ledger', price: '249.00', priceCents: 24900, image: '📒', description: 'Financial secretary' },
    { id: 'concierge', name: 'Concierge', price: '199.00', priceCents: 19900, image: '🔑', description: '24/7 global concierge' },
    { id: 'closeter', name: 'Closeter', price: '399.00', priceCents: 39900, image: '💼', description: 'Sales support specialist' },
    { id: 'velvet', name: 'Velvet', price: '599.00', priceCents: 59900, image: '✨', description: 'Premium white-glove service' },
    { id: 'executive', name: 'Executive', price: '599.00', priceCents: 59900, image: '👔', description: 'C-suite executive assistant' }
];

// Add to cart buttons
document.querySelectorAll('.add-to-cart').forEach(btn => {
    btn.addEventListener('click', (e) => {
        const productId = e.target.dataset.productId;
        const product = products.find(p => p.id === productId);
        if (product) {
            cart.addItem(product);
        }
    });
});

// Initialize on cart page
if (document.getElementById('cart-items')) {
    cart.renderCartPage();
}
