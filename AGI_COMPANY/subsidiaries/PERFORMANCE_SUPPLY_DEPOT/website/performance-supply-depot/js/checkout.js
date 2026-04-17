/**
 * PSDEPOT Checkout System
 * Stripe integration with billing/shipping addresses
 * Google Sign-In, Phone Lookup
 */

// Stripe configuration (loaded from backend)
let stripe = null;
let cardElement = null;
let paymentConfig = {
    publishableKey: 'pk_test_TYooMQauvdEDq54NiTphI7jx', // Test key - replace with live
    shippingRate: 15.56
};

// API base URL
const API_BASE = 'https://myl0nr0s.cloud/api'; // Update with your domain

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadCartDisplay();
    await initializeStripe();
    setupEventListeners();
});

// Load cart display with shipping calculation
async function loadCartDisplay() {
    const cart = JSON.parse(localStorage.getItem('agi_cart') || '[]');
    const container = document.getElementById('cart-items-container');
    
    if (!container) return;

    if (cart.length === 0) {
        container.innerHTML = `
            <div class="empty-cart">
                <h3>Your cart is empty</h3>
                <p>Add some AGI agents to get started!</p>
                <a href="products.html" class="btn-primary" style="display: inline-block; width: auto; text-decoration: none;">Browse Products</a>
            </div>
        `;
        document.getElementById('payment-section').style.display = 'none';
        return;
    }

    let html = '<div class="cart-items-list">';
    let subtotal = 0;
    let totalQuantity = 0;

    cart.forEach(item => {
        const itemPrice = item.priceCents / 100;
        const itemTotal = itemPrice * item.quantity;
        subtotal += itemTotal;
        totalQuantity += item.quantity;
        
        html += `
            <div class="cart-item">
                <div class="item-product">
                    <span class="emoji">${item.image || '📦'}</span>
                    <div>
                        <div class="name">${item.name}</div>
                        <button class="remove-btn" onclick="removeFromCart('${item.id}')">Remove</button>
                    </div>
                </div>
                <div class="item-qty">
                    <input type="number" value="${item.quantity}" min="1" 
                           onchange="updateQuantity('${item.id}', this.value)" 
                           style="width: 60px; text-align: center;">
                </div>
                <div class="item-price">$${itemPrice.toFixed(2)}</div>
                <div class="item-total">$${itemTotal.toFixed(2)}</div>
            </div>
        `;
    });

    html += '</div>';
    container.innerHTML = html;

    // Calculate totals
    const shipping = totalQuantity * 15.56;
    // Tax will be calculated based on shipping address
    const taxResult = await calculateTax(subtotal, shipping);
    const tax = taxResult.tax_amount;
    const total = subtotal + shipping + tax;

    // Update displays
    document.getElementById('cart-subtotal').textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById('cart-shipping').textContent = `$${shipping.toFixed(2)}`;
    document.getElementById('cart-tax').textContent = `$${tax.toFixed(2)}`;
    if (taxResult.tax_rate > 0) {
        const taxLabel = document.querySelector('.total-line.tax small');
        if (taxLabel) taxLabel.textContent = `(${(taxResult.tax_rate * 100).toFixed(2)}% CA)`;
    }
    document.getElementById('cart-total').textContent = `$${total.toFixed(2)}`;

    // Update header cart count
    const cartCount = document.getElementById('cart-count');
    if (cartCount) {
        cartCount.textContent = totalQuantity;
        cartCount.style.display = totalQuantity > 0 ? 'inline' : 'none';
    }
}

// Calculate tax based on shipping address
async function calculateTax(subtotal, shipping) {
    const state = document.getElementById('shipping-state')?.value || 
                  document.getElementById('billing-state')?.value || '';
    
    if (!state) {
        return { tax_amount: 0, tax_rate: 0 };
    }
    
    try {
        const response = await fetch(`${API_BASE}/calculate-tax`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                subtotal: Math.round(subtotal * 100), // cents
                shipping: Math.round(shipping * 100), // cents (non-taxable)
                address: { state: state }
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            return { tax_amount: data.tax_amount / 100, tax_rate: data.tax_rate };
        }
    } catch (e) {
        console.log('Tax calculation failed, using 0%');
    }
    
    return { tax_amount: 0, tax_rate: 0 };
}

// Update tax when state changes
document.addEventListener('change', async (e) => {
    if (e.target.id === 'billing-state' || e.target.id === 'shipping-state') {
        await loadCartDisplay();
    }
});

// Initialize Stripe
async function initializeStripe() {
    if (typeof Stripe === 'undefined') {
        console.error('Stripe.js not loaded');
        return;
    }

    stripe = Stripe(paymentConfig.publishableKey);
    const elements = stripe.elements();
    
    cardElement = elements.create('card', {
        style: {
            base: {
                fontSize: '16px',
                color: '#2d3748',
                '::placeholder': {
                    color: '#a0aec0'
                }
            },
            invalid: {
                color: '#e53e3e',
                iconColor: '#e53e3e'
            }
        }
    });
    
    const cardContainer = document.getElementById('card-element');
    if (cardContainer) {
        cardElement.mount('#card-element');
        
        cardElement.on('change', (event) => {
            const errorElement = document.getElementById('card-errors');
            if (event.error) {
                errorElement.textContent = event.error.message;
            } else {
                errorElement.textContent = '';
            }
        });
    }
}

// Phone lookup for business information
async function lookupBusiness() {
    const phoneInput = document.getElementById('billing-phone');
    const phone = phoneInput?.value?.trim();
    
    if (!phone) {
        alert('Please enter a phone number');
        return;
    }
    
    const lookupBtn = event.target;
    lookupBtn.disabled = true;
    lookupBtn.textContent = 'Looking up...';
    
    try {
        const response = await fetch(`${API_BASE}/lookup-business`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ phone: phone })
        });
        
        const data = await response.json();
        
        if (data.found && data.business) {
            // Auto-fill billing address
            document.getElementById('billing-company').value = data.business.name || '';
            document.getElementById('billing-street').value = data.business.address?.street || '';
            document.getElementById('billing-city').value = data.business.address?.city || '';
            document.getElementById('billing-state').value = data.business.address?.state || '';
            document.getElementById('billing-zip').value = data.business.address?.zip || '';
            
            // Show found notification
            const foundDiv = document.getElementById('business-found');
            const nameSpan = document.getElementById('business-name');
            const addrSpan = document.getElementById('business-address');
            
            if (foundDiv && nameSpan && addrSpan) {
                nameSpan.textContent = data.business.name;
                addrSpan.textContent = `${data.business.address?.street}, ${data.business.address?.city}, ${data.business.address?.state} ${data.business.address?.zip}`;
                foundDiv.classList.add('show');
            }
        } else {
            alert('Business not found. Please enter your address manually.');
        }
    } catch (error) {
        console.error('Lookup error:', error);
        alert('Unable to lookup business. Please enter your address manually.');
    } finally {
        lookupBtn.disabled = false;
        lookupBtn.textContent = '🔍 Lookup';
    }
}

// Toggle shipping address visibility
function toggleShippingAddress() {
    const checkbox = document.getElementById('same-as-billing');
    const form = document.getElementById('shipping-address-form');
    
    if (checkbox && form) {
        if (checkbox.checked) {
            form.style.display = 'none';
            // Copy billing to shipping
            copyAddress('billing', 'shipping');
        } else {
            form.style.display = 'block';
        }
    }
}

// Copy address fields
function copyAddress(from, to) {
    const fields = ['name', 'company', 'street', 'city', 'state', 'zip', 'country'];
    fields.forEach(field => {
        const fromEl = document.getElementById(`${from}-${field}`);
        const toEl = document.getElementById(`${to}-${field}`);
        if (fromEl && toEl) {
            toEl.value = fromEl.value;
        }
    });
}

// Google Sign-In (placeholder - requires Google Cloud setup)
function signInWithGoogle() {
    // TODO: Implement Google OAuth2
    // Requires: Google Cloud Console setup, OAuth2 credentials, redirect URI
    alert('Google Sign-In coming soon! Please use manual checkout for now.');
    
    // When implemented:
    // window.location.href = 'https://accounts.google.com/o/oauth2/v2/auth?' +
    //     'client_id=YOUR_CLIENT_ID&' +
    //     'redirect_uri=YOUR_REDIRECT_URI&' +
    //     'scope=email profile&' +
    //     'response_type=token';
}

// Process payment
async function processPayment() {
    const btn = document.getElementById('checkout-button');
    const cart = JSON.parse(localStorage.getItem('agi_cart') || '[]');
    
    if (cart.length === 0) {
        alert('Your cart is empty!');
        return;
    }
    
    // Validate required fields
    const requiredFields = ['billing-name', 'billing-email', 'billing-street', 'billing-city', 'billing-state', 'billing-zip'];
    const missing = requiredFields.filter(id => !document.getElementById(id)?.value?.trim());
    
    if (missing.length > 0) {
        alert('Please fill in all required billing fields');
        return;
    }
    
    btn.disabled = true;
    btn.textContent = 'Processing...';
    
    try {
        // Prepare addresses
        const billingAddress = {
            name: document.getElementById('billing-name').value,
            line1: document.getElementById('billing-street').value,
            line2: document.getElementById('billing-company').value || '',
            city: document.getElementById('billing-city').value,
            state: document.getElementById('billing-state').value,
            zip: document.getElementById('billing-zip').value,
            country: document.getElementById('billing-country').value
        };
        
        const shippingAddress = document.getElementById('same-as-billing')?.checked ? 
            billingAddress : {
                name: document.getElementById('shipping-name').value,
                line1: document.getElementById('shipping-street').value,
                line2: document.getElementById('shipping-company').value || '',
                city: document.getElementById('shipping-city').value,
                state: document.getElementById('shipping-state').value,
                zip: document.getElementById('shipping-zip').value,
                country: document.getElementById('shipping-country').value
            };
        
        const customerEmail = document.getElementById('billing-email').value;
        const customerPhone = document.getElementById('billing-phone')?.value || '';
        
        // Create payment intent
        const response = await fetch(`${API_BASE}/create-payment-intent`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                items: cart,
                shipping_address: shippingAddress,
                billing_address: billingAddress,
                email: customerEmail,
                phone: customerPhone
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Payment failed');
        }
        
        const { clientSecret } = await response.json();
        
        // Confirm card payment
        const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: cardElement,
                billing_details: {
                    name: billingAddress.name,
                    email: customerEmail,
                    address: {
                        line1: billingAddress.line1,
                        line2: billingAddress.line2,
                        city: billingAddress.city,
                        state: billingAddress.state,
                        postal_code: billingAddress.zip,
                        country: billingAddress.country
                    }
                }
            }
        });
        
        if (error) {
            throw new Error(error.message);
        }
        
        if (paymentIntent.status === 'succeeded') {
            // Clear cart
            localStorage.removeItem('agi_cart');
            
            // Show success
            alert(`Payment successful! Order ID: ${paymentIntent.id}`);
            window.location.href = `success.html?order=${paymentIntent.id}`;
        } else {
            throw new Error('Payment not completed');
        }
        
    } catch (error) {
        console.error('Payment error:', error);
        document.getElementById('card-errors').textContent = error.message;
        btn.disabled = false;
        btn.textContent = 'Complete Purchase';
    }
}

// Remove item from cart
function removeFromCart(productId) {
    let cart = JSON.parse(localStorage.getItem('agi_cart') || '[]');
    cart = cart.filter(item => item.id !== productId);
    localStorage.setItem('agi_cart', JSON.stringify(cart));
    loadCartDisplay();
}

// Update quantity
function updateQuantity(productId, quantity) {
    const qty = parseInt(quantity);
    if (qty < 1) return;
    
    let cart = JSON.parse(localStorage.getItem('agi_cart') || '[]');
    const item = cart.find(i => i.id === productId);
    if (item) {
        item.quantity = qty;
        localStorage.setItem('agi_cart', JSON.stringify(cart));
        loadCartDisplay();
    }
}

// Setup event listeners
function setupEventListeners() {
    // Address sync when "same as billing" is checked
    const billingFields = ['billing-name', 'billing-street', 'billing-city', 'billing-state', 'billing-zip', 'billing-country'];
    billingFields.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('change', () => {
                if (document.getElementById('same-as-billing')?.checked) {
                    copyAddress('billing', 'shipping');
                }
            });
        }
    });
}

// Make functions available globally
window.lookupBusiness = lookupBusiness;
window.toggleShippingAddress = toggleShippingAddress;
window.signInWithGoogle = signInWithGoogle;
window.processPayment = processPayment;
window.removeFromCart = removeFromCart;
window.updateQuantity = updateQuantity;
