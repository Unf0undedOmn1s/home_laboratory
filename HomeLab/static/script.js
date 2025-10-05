// Global variables
let allPasswords = [];
let filteredPasswords = [];

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadPasswords();
    setupEventListeners();
});

function setupEventListeners() {
    // File upload
    const fileInput = document.getElementById('fileInput');
    if (fileInput) {
        fileInput.addEventListener('change', handleFileUpload);
    }
    
    // Search
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', handleSearch);
    }
}

// Show toast notification
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    if (!toast) return;
    
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    
    setTimeout(() => {
        toast.className = 'toast';
    }, 3000);
}

// Handle file upload
async function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showToast(data.message, 'success');
            loadPasswords();
        } else {
            showToast(data.error || 'Upload failed', 'error');
        }
    } catch (error) {
        showToast('Error uploading file: ' + error.message, 'error');
        console.error('Upload error:', error);
    }
    
    // Reset file input
    event.target.value = '';
}

// Load passwords from server
async function loadPasswords() {
    console.log('Loading passwords...'); // Debug log
    try {
        const response = await fetch('/api/passwords');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Get the raw text first to debug
        const text = await response.text();
        console.log('Response received, length:', text.length); // Debug log
        
        // Try to parse it as JSON
        let data;
        try {
            data = JSON.parse(text);
            console.log('Parsed data:', data); // Debug log
        } catch (parseError) {
            console.error('JSON Parse Error:', parseError);
            console.error('Response text:', text);
            showToast('Error: Invalid response from server', 'error');
            return;
        }
        
        allPasswords = data.data || [];
        filteredPasswords = data.data || [];
        
        console.log('Passwords loaded:', allPasswords.length); // Debug log
        
        updateStats(data.total || 0, data.filtered || 0);
        displayPasswords(filteredPasswords);
    } catch (error) {
        console.error('Error loading passwords:', error);
        showToast('Error loading data: ' + error.message, 'error');
        
        // Initialize with empty data
        allPasswords = [];
        filteredPasswords = [];
        updateStats(0, 0);
        displayPasswords([]);
    }
}

// Display passwords in table
function displayPasswords(passwords) {
    const noData = document.getElementById('noData');
    const tableWrapper = document.getElementById('tableWrapper');
    const tableHead = document.getElementById('tableHead');
    const tableBody = document.getElementById('tableBody');
    
    console.log('Displaying passwords:', passwords); // Debug log
    
    if (!passwords || passwords.length === 0) {
        if (noData) noData.style.display = 'block';
        if (tableWrapper) tableWrapper.style.display = 'none';
        const columnsElement = document.getElementById('columnsCount');
        if (columnsElement) columnsElement.textContent = '0';
        return;
    }
    
    if (noData) noData.style.display = 'none';
    if (tableWrapper) tableWrapper.style.display = 'block';
    
    // Get columns from first entry (exclude _id)
    const allColumns = Object.keys(passwords[0]).filter(col => col !== '_id');
    const columns = allColumns;
    console.log('Columns found:', columns); // Debug log
    
    const columnsElement = document.getElementById('columnsCount');
    if (columnsElement) columnsElement.textContent = columns.length;
    
    // Create table header
    if (tableHead) {
        tableHead.innerHTML = '';
        const headerRow = document.createElement('tr');
        columns.forEach(col => {
            const th = document.createElement('th');
            th.textContent = col;
            headerRow.appendChild(th);
        });
        
        // Add Actions column
        const actionsHeader = document.createElement('th');
        actionsHeader.textContent = 'Actions';
        headerRow.appendChild(actionsHeader);
        
        tableHead.appendChild(headerRow);
    }
    
    // Create table body
    if (tableBody) {
        tableBody.innerHTML = '';
        passwords.forEach((entry, index) => {
            const row = document.createElement('tr');
            
            columns.forEach(col => {
                const td = document.createElement('td');
                const value = entry[col];
                
                // Display value or empty string
                if (value !== undefined && value !== null && value !== '') {
                    td.textContent = value;
                } else {
                    td.textContent = '';
                    td.style.opacity = '0.3';
                }
                
                td.title = 'Click to copy';
                td.addEventListener('click', () => {
                    if (value && value !== '') {
                        copyToClipboard(value);
                    }
                });
                row.appendChild(td);
            });
            
            // Add action buttons
            const actionsTd = document.createElement('td');
            actionsTd.innerHTML = `
                <div class="action-buttons">
                    <button class="btn btn-danger btn-small" onclick="deletePassword(${entry._id})">
                        🗑️ Delete
                    </button>
                </div>
            `;
            row.appendChild(actionsTd);
            
            tableBody.appendChild(row);
        });
        
        console.log('Table rendered with', passwords.length, 'rows'); // Debug log
    }
}

// Update statistics
function updateStats(total, filtered) {
    const totalElement = document.getElementById('totalEntries');
    const filteredElement = document.getElementById('displayedEntries');
    
    if (totalElement) {
        totalElement.textContent = total;
    }
    
    if (filteredElement) {
        filteredElement.textContent = filtered;
    }
}

// Handle search
async function handleSearch(event) {
    const query = event.target.value;
    
    try {
        const response = await fetch(`/api/passwords?search=${encodeURIComponent(query)}`);
        
        if (!response.ok) {
            throw new Error('Search failed');
        }
        
        const data = await response.json();
        
        filteredPasswords = data.data || [];
        updateStats(data.total || 0, data.filtered || 0);
        displayPasswords(filteredPasswords);
    } catch (error) {
        console.error('Error searching:', error);
        showToast('Search error', 'error');
    }
}

// Copy to clipboard
function copyToClipboard(text) {
    if (!text) return;
    
    // Check if clipboard API is available
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('Copied to clipboard!', 'success');
        }).catch(err => {
            console.error('Clipboard error:', err);
            fallbackCopyToClipboard(text);
        });
    } else {
        fallbackCopyToClipboard(text);
    }
}

// Fallback copy method for older browsers
function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showToast('Copied to clipboard!', 'success');
        } else {
            showToast('Failed to copy', 'error');
        }
    } catch (err) {
        console.error('Fallback copy failed:', err);
        showToast('Failed to copy', 'error');
    }
    
    document.body.removeChild(textArea);
}

// Show logs modal
async function showLogs() {
    const modal = document.getElementById('logsModal');
    const logsContent = document.getElementById('logsContent');
    
    if (!modal || !logsContent) return;
    
    try {
        const response = await fetch('/api/logs');
        
        if (!response.ok) {
            throw new Error('Failed to load logs');
        }
        
        const data = await response.json();
        
        logsContent.innerHTML = '';
        
        if (!data.logs || data.logs.length === 0) {
            logsContent.innerHTML = '<div class="log-entry">No logs available</div>';
        } else {
            data.logs.forEach(log => {
                const logEntry = document.createElement('div');
                logEntry.className = 'log-entry';
                logEntry.innerHTML = `
                    <span class="log-timestamp">${log.timestamp}</span>
                    <span>${log.message}</span>
                `;
                logsContent.appendChild(logEntry);
            });
        }
        
        modal.style.display = 'block';
    } catch (error) {
        console.error('Error loading logs:', error);
        showToast('Error loading logs', 'error');
    }
}

// Close logs modal
function closeLogs() {
    const modal = document.getElementById('logsModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('logsModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}

// Export data
async function exportData() {
    try {
        const response = await fetch('/api/export');
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'vault_export.csv';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showToast('Data exported successfully!', 'success');
        } else {
            const data = await response.json();
            showToast(data.error || 'Export failed', 'error');
        }
    } catch (error) {
        console.error('Export error:', error);
        showToast('Error exporting data', 'error');
    }
}

// Export logs
async function exportLogs() {
    try {
        const response = await fetch('/api/export-logs');
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'vault_logs.txt';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showToast('Logs exported successfully!', 'success');
            closeLogs();
        } else {
            const data = await response.json();
            showToast(data.error || 'Export failed', 'error');
        }
    } catch (error) {
        console.error('Export logs error:', error);
        showToast('Error exporting logs', 'error');
    }
}

// Clear all data
async function clearData() {
    if (!confirm('Are you sure you want to clear all data? This cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch('/api/clear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error('Clear failed');
        }
        
        const data = await response.json();
        
        showToast(data.message || 'All data cleared', 'success');
        loadPasswords();
    } catch (error) {
        console.error('Clear error:', error);
        showToast('Error clearing data', 'error');
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + K to focus search
    if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to close modal
    if (event.key === 'Escape') {
        closeLogs();
        closePasswordModal();
    }
});

// Show add password modal
function showAddModal() {
    const modal = document.getElementById('passwordModal');
    const form = document.getElementById('passwordForm');
    
    if (modal && form) {
        form.reset();
        document.getElementById('modalTitle').textContent = '➕ Add New Password';
        modal.style.display = 'block';
    }
}

// Close password modal
function closePasswordModal() {
    const modal = document.getElementById('passwordModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Save password
async function savePassword() {
    const form = document.getElementById('passwordForm');
    if (!form) return;
    
    const formData = new FormData(form);
    const data = {};
    
    // Convert form data to object
    formData.forEach((value, key) => {
        data[key] = value;
    });
    
    // Validate required fields
    if (!data.name || data.name.trim() === '') {
        showToast('Name is required', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/passwords/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showToast(result.message || 'Password added successfully', 'success');
            closePasswordModal();
            loadPasswords();
        } else {
            showToast(result.error || 'Failed to add password', 'error');
        }
    } catch (error) {
        console.error('Error adding password:', error);
        showToast('Error adding password: ' + error.message, 'error');
    }
}

// Delete password
async function deletePassword(index) {
    if (!confirm('Are you sure you want to delete this password entry?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/passwords/delete/${index}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showToast(result.message || 'Password deleted successfully', 'success');
            loadPasswords();
        } else {
            showToast(result.error || 'Failed to delete password', 'error');
        }
    } catch (error) {
        console.error('Error deleting password:', error);
        showToast('Error deleting password: ' + error.message, 'error');
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const logsModal = document.getElementById('logsModal');
    const passwordModal = document.getElementById('passwordModal');
    
    if (event.target === logsModal) {
        logsModal.style.display = 'none';
    }
    if (event.target === passwordModal) {
        passwordModal.style.display = 'none';
    }
}

// Auto-refresh data every 30 seconds (optional)
// Uncomment if you want auto-refresh
// setInterval(loadPasswords, 30000);