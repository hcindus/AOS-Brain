const axios = require('axios');
const crypto = require('crypto');

/**
 * Check if password has been breached using Have I Been Pwned API
 * Uses k-anonymity to protect password privacy
 */
async function checkPasswordBreach(password) {
    try {
        // Hash password with SHA-1
        const hash = crypto.createHash('sha1').update(password).digest('hex').toUpperCase();
        
        // Use k-anonymity: send first 5 characters
        const prefix = hash.substring(0, 5);
        const suffix = hash.substring(5);
        
        const response = await axios.get(
            `https://api.pwnedpasswords.com/range/${prefix}`,
            { timeout: 5000 }
        );
        
        // Check if suffix exists in response
        const hashes = response.data.split('\n');
        for (const line of hashes) {
            const [hashSuffix, count] = line.split(':');
            if (hashSuffix === suffix) {
                return {
                    breached: true,
                    count: parseInt(count, 10)
                };
            }
        }
        
        return { breached: false, count: 0 };
    } catch (err) {
        // Fail open - if API is down, don't block registration
        console.error('Breach check failed:', err.message);
        return { breached: false, count: 0, error: true };
    }
}

module.exports = {
    checkPasswordBreach
};