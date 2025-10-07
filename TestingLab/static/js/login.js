document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const masterPassword = document.getElementById('masterPassword').value;
    const errorDiv = document.getElementById('errorMessage');
    
    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ master_password: masterPassword })
        });
        
        const data = await response.json();
        
        if (data.success) {
            window.location.href = '/';
        } else {
            errorDiv.textContent = data.error || 'Invalid master password';
            errorDiv.style.display = 'block';
        }
    } catch (error) {
        errorDiv.textContent = 'Network error. Please try again.';
        errorDiv.style.display = 'block';
    }
});

// Auto-focus password field
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('masterPassword').focus();
});