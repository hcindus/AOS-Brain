/**
 * STRIPE CHECKOUT INTEGRATION
 * Real payment processing with Stripe
 */

const STRIPE_PUBLISHABLE_KEY = 'pk_test_TYooMQauvdEDq54NiTphI7jx'; // Replace with your actual key
const API_BASE_URL = 'https://myl0nr0s.cloud/api'; // Your backend API

let stripe;
let elements;
let cardElement;

// Initialize Stripe
function initializeStripe() {
    stripe = Stripe(STRIPE_PUBLISHABLE_KEY);
    elements = stripe.elements();
    
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
    
    cardElement.mount('#card-element');
    
    // Handle validation errors
    cardElement.on('change', (event) => {
        const errorElement = document.getElementById('card-errors');
        if (event.error) {
            errorElement.textContent = event.error.message;
        } else {
            errorElement.textContent = '';
        }
    });
}

// Create payment intent
document.getElementById('payment-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const submitButton = document.getElementById('submit-button');
    const spinner = document.getElementById('spinner');
    
    submitButton.disabled = true;
    spinner.style.display = 'block';
    
    try {
        // Get cart items
        const cart = JSON.parse(localStorage.getItem('agi_cart') || '[]');
        const total = cart.reduce((sum, item) => sum + (item.priceCents * item.quantity), 0);
        
        if (total === 0) {
            throw new Error('Cart is empty');
        }
        
        // Create payment intent
        const response = await fetch(`${API_BASE_URL}/create-payment-intent`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                amount: total,
                currency: 'usd',
                items: cart.map(item => ({
                    id: item.id,
                    name: item.name,
                    quantity: item.quantity,
                    price: item.priceCents
                }))
            })
        });
        
        const { clientSecret } = await response.json();
        
        // Confirm card payment
        const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: cardElement,
                billing_details: {
                    name: document.getElementById('name').value || 'Customer',
                    email: document.getElementById('email').value || 'customer@example.com'
                }
            }
        });
        
        if (error) {
            document.getElementById('card-errors').textContent = error.message;
            submitButton.disabled = false;
            spinner.style.display = 'none';
        } else {
            // Payment successful
            document.getElementById('payment-success').style.display = 'block';
            document.getElementById('payment-form').style.display = 'none';
            
            // Clear cart
            localStorage.removeItem('agi_cart');
            
            // Show success message
            showSuccessMessage(paymentIntent.id);
            
            // Redirect after 3 seconds
            setTimeout(() => {
                window.location.href = 'success.html?order=' + paymentIntent.id;
            }, 3000);
        }
    } catch (error) {
        console.error('Payment error:', error);
        document.getElementById('card-errors').textContent = 'Payment failed. Please try again.';
        submitButton.disabled = false;
        spinner.style.display = 'none';
    }
});

// Show success message
function showSuccessMessage(paymentIntentId) {
    const successDiv = document.getElementById('payment-success');
    if (successDiv) {
        successDiv.innerHTML = `
            <div style="background: #d1fae5; border: 1px solid #10b981; padding: 20px; border-radius: 8px; margin-top: 20px;">
                <h3 style="color: #065f46; margin: 0 0 10px 0;">✓ Payment Successful!</h3>
                <p style="color: #047857; margin: 0;">Order ID: ${paymentIntentId}</p>
                <p style="color: #047857; margin: 10px 0 0 0;">Redirecting to your dashboard...</p>
            </div>
        `;
    }
}

// Alternative: Crypto payment
document.getElementById('crypto-payment')?.addEventListener('click', async () => {
    const cart = JSON.parse(localStorage.getItem('agi_cart') || '[]');
    const totalUSD = cart.reduce((sum, item) => sum + (item.priceCents * item.quantity), 0) / 100;
    
    // Convert USD to ETH (example - you'd use real exchange rate)
    const ethPrice = 3500; // Example ETH price
    const ethAmount = (totalUSD / ethPrice).toFixed(6);
    
    const walletAddress = '0x742d35Cc6634C0532925a3b844Bc9e7595f8dEe'; // Your wallet
    
    // Show crypto payment modal
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10000;
    `;
    
    modal.innerHTML = `
        <div style="background: white; padding: 40px; border-radius: 12px; max-width: 500px; text-align: center;">
            <h3 style="color: #1a365d; margin-bottom: 20px;">Pay with Crypto</h3>
            <p style="color: #718096; margin-bottom: 20px;">Send ${ethAmount} ETH to:</p>
            <div style="background: #f7fafc; padding: 15px; border-radius: 8px; font-family: monospace; word-break: break-all; margin-bottom: 20px;">
                ${walletAddress}
            </div>
            <button onclick="this.parentElement.parentElement.remove()" style="background: #ed8936; color: white; border: none; padding: 12px 30px; border-radius: 6px; cursor: pointer;">Close</button>
        </div>
    `;
    
    document.body.appendChild(modal);
});

// Initialize on page load
if (document.getElementById('card-element')) {
    initializeStripe();
}
