class PasswordVault {
    constructor() {
        this.passwords = [];
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadPasswords();
    }

    bindEvents() {
        document.getElementById('addPasswordBtn').addEventListener('click', () => this.showModal());
        document.getElementById('cancelBtn').addEventListener('click', () => this.hideModal());
        document.querySelector('.close').addEventListener('click', () => this.hideModal());
        document.getElementById('passwordForm').addEventListener('submit', (e) => this.savePassword(e));
        document.getElementById('searchInput').addEventListener('input', (e) => this.searchPasswords(e.target.value));
        
        // Close modal when clicking outside
        document.getElementById('passwordModal').addEventListener('click', (e) => {
            if (e.target.id === 'passwordModal') {
                this.hideModal();
            }
        });
    }

    async loadPasswords() {
        try {
            const response = await fetch('/passwords');
            if (response.ok) {
                this.passwords = await response.json();
                this.renderPasswords();
            } else {
                throw new Error('Failed to load passwords');
            }
        } catch (error) {
            console.error('Error loading passwords:', error);
            alert('Error loading passwords');
        }
    }

    renderPasswords(passwords = this.passwords) {
        const grid = document.getElementById('passwordsGrid');
        
        if (passwords.length === 0) {
            grid.innerHTML = '<div class="no-passwords">No passwords stored yet. Click "Add Password" to get started.</div>';
            return;
        }

        grid.innerHTML = passwords.map(password => `
            <div class="password-card">
                <div class="password-header">
                    <div>
                        <div class="password-name">${this.escapeHtml(password.name)}</div>
                        ${password.url ? `<div class="password-url">${this.escapeHtml(password.url)}</div>` : ''}
                    </div>
                </div>
                
                <div class="password-field">
                    <div class="field-label">Username</div>
                    <div class="field-value">
                        <span>${this.escapeHtml(password.username)}</span>
                        <button class="copy-btn" onclick="vault.copyToClipboard('${this.escapeHtml(password.username)}')" title="Copy username">
                            📋
                        </button>
                    </div>
                </div>
                
                <div class="password-field">
                    <div class="field-label">Password</div>
                    <div class="field-value">
                        <span class="password-masked">••••••••</span>
                        <button class="copy-btn" onclick="vault.copyToClipboard('${this.escapeHtml(password.password)}')" title="Copy password">
                            📋
                        </button>
                        <button class="copy-btn" onclick="vault.togglePassword(this, '${this.escapeHtml(password.password)}')" title="Show password">
                            👁️
                        </button>
                    </div>
                </div>
                
                ${password.notes ? `
                <div class="password-field">
                    <div class="field-label">Notes</div>
                    <div>${this.escapeHtml(password.notes)}</div>
                </div>
                ` : ''}
                
                <button class="delete-btn" onclick="vault.deletePassword(${password.id})">
                    Delete
                </button>
            </div>
        `).join('');
    }

    showModal() {
        document.getElementById('passwordModal').style.display = 'flex';
        document.getElementById('passwordForm').reset();
    }

    hideModal() {
        document.getElementById('passwordModal').style.display = 'none';
    }

    async savePassword(e) {
        e.preventDefault();
        
        const passwordData = {
            name: document.getElementById('name').value,
            username: document.getElementById('username').value,
            password: document.getElementById('password').value,
            url: document.getElementById('url').value,
            notes: document.getElementById('notes').value
        };

        try {
            const response = await fetch('/passwords', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(passwordData)
            });

            if (response.ok) {
                this.hideModal();
                this.loadPasswords();
            } else {
                throw new Error('Failed to save password');
            }
        } catch (error) {
            console.error('Error saving password:', error);
            alert('Error saving password');
        }
    }

    async deletePassword(id) {
        if (!confirm('Are you sure you want to delete this password?')) {
            return;
        }

        try {
            const response = await fetch(`/passwords/${id}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                this.loadPasswords();
            } else {
                throw new Error('Failed to delete password');
            }
        } catch (error) {
            console.error('Error deleting password:', error);
            alert('Error deleting password');
        }
    }

    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            // Show feedback
            const btn = event.target;
            const original = btn.innerHTML;
            btn.innerHTML = '✅';
            setTimeout(() => btn.innerHTML = original, 1000);
        } catch (error) {
            console.error('Failed to copy:', error);
            alert('Failed to copy to clipboard');
        }
    }

    togglePassword(button, password) {
        const fieldValue = button.parentElement;
        const maskedSpan = fieldValue.querySelector('.password-masked');
        
        if (maskedSpan.style.display !== 'none') {
            maskedSpan.style.display = 'none';
            const plainText = document.createElement('span');
            plainText.textContent = password;
            plainText.className = 'password-plain';
            fieldValue.insertBefore(plainText, maskedSpan);
            button.title = 'Hide password';
        } else {
            const plainText = fieldValue.querySelector('.password-plain');
            plainText.remove();
            maskedSpan.style.display = 'inline';
            button.title = 'Show password';
        }
    }

    searchPasswords(query) {
        const filtered = this.passwords.filter(password => 
            password.name.toLowerCase().includes(query.toLowerCase()) ||
            password.username.toLowerCase().includes(query.toLowerCase()) ||
            (password.url && password.url.toLowerCase().includes(query.toLowerCase())) ||
            (password.notes && password.notes.toLowerCase().includes(query.toLowerCase()))
        );
        this.renderPasswords(filtered);
    }

    escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
}

// Initialize the vault when the page loads
const vault = new PasswordVault();