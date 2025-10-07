# app.py
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_this_in_production'

# Admin credentials from environment variables
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

# Encryption setup
def generate_key():
    # Use a fixed salt for simplicity
    salt = b'homelab_vault_salt_12345'
    password = b'homelab_master_key_12345'
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password))

ENCRYPTION_KEY = generate_key()

def encrypt_password(password: str) -> str:
    fernet = Fernet(ENCRYPTION_KEY)
    encrypted = fernet.encrypt(password.encode())
    return base64.urlsafe_b64encode(encrypted).decode()

def decrypt_password(encrypted_password: str) -> str:
    fernet = Fernet(ENCRYPTION_KEY)
    encrypted = base64.urlsafe_b64decode(encrypted_password.encode())
    return fernet.decrypt(encrypted).decode()

# Database setup
def init_db():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT NOT NULL,
            encrypted_password TEXT NOT NULL,
            url TEXT,
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Authentication check
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/passwords', methods=['GET'])
@login_required
def get_passwords():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    
    c.execute("SELECT id, name, username, encrypted_password, url, notes FROM passwords")
    passwords = []
    
    for row in c.fetchall():
        try:
            decrypted_password = decrypt_password(row[3])
            passwords.append({
                'id': row[0],
                'name': row[1],
                'username': row[2],
                'password': decrypted_password,
                'url': row[4],
                'notes': row[5]
            })
        except:
            continue
    
    conn.close()
    return jsonify(passwords)

@app.route('/passwords', methods=['POST'])
@login_required
def add_password():
    data = request.get_json()
    encrypted_password = encrypt_password(data['password'])
    
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO passwords (name, username, encrypted_password, url, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['name'], data['username'], encrypted_password, data.get('url', ''), data.get('notes', '')))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/passwords/<int:password_id>', methods=['DELETE'])
@login_required
def delete_password(password_id):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    
    c.execute("DELETE FROM passwords WHERE id = ?", (password_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

if __name__ == '__main__':
    init_db()
    print("Admin Password Vault starting...")
    print(f"Admin username: {ADMIN_USERNAME}")
    print("Access at: http://localhost:5000")
    print("Login required with admin credentials")
    app.run(debug=True, host='0.0.0.0', port=5000)