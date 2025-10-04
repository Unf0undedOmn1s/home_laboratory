from flask import Flask, render_template, request, redirect, url_for, session, flash
from cryptography.fernet import Fernet
import sqlite3
import bcrypt
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=30)

# Generate or load encryption key
def get_encryption_key():
    if not os.path.exists('secret.key'):
        key = Fernet.generate_key()
        with open('secret.key', 'wb') as key_file:
            key_file.write(key)
    else:
        with open('secret.key', 'rb') as key_file:
            key = key_file.read()
    return key

cipher_suite = Fernet(get_encryption_key())

# Database initialization
def init_db():
    conn = sqlite3.connect('vault.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # Passwords table
    c.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            service_name TEXT NOT NULL,
            username TEXT NOT NULL,
            encrypted_password TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Encryption functions
def encrypt_password(password):
    return cipher_suite.encrypt(password.encode())

def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password).decode()

# Authentication routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long')
            return redirect(url_for('register'))
        
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        
        try:
            conn = sqlite3.connect('vault.db')
            c = conn.cursor()
            c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                     (username, password_hash))
            conn.commit()
            conn.close()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('vault.db')
        c = conn.cursor()
        c.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        
        if user and bcrypt.checkpw(password.encode(), user[1]):
            session.permanent = True
            session['user_id'] = user[0]
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('login'))

# Password management routes
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('vault.db')
    c = conn.cursor()
    c.execute('''
        SELECT id, service_name, username, notes 
        FROM passwords WHERE user_id = ?
    ''', (session['user_id'],))
    passwords = c.fetchall()
    conn.close()
    
    return render_template('dashboard.html', passwords=passwords)

@app.route('/add_password', methods=['GET', 'POST'])
def add_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        service_name = request.form['service_name']
        username = request.form['username']
        password = request.form['password']
        notes = request.form.get('notes', '')
        
        encrypted_password = encrypt_password(password)
        
        conn = sqlite3.connect('vault.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO passwords (user_id, service_name, username, encrypted_password, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (session['user_id'], service_name, username, encrypted_password, notes))
        conn.commit()
        conn.close()
        
        flash('Password added successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('add_password.html')

@app.route('/view_password/<int:password_id>')
def view_password(password_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('vault.db')
    c = conn.cursor()
    c.execute('''
        SELECT service_name, username, encrypted_password, notes 
        FROM passwords WHERE id = ? AND user_id = ?
    ''', (password_id, session['user_id']))
    password_data = c.fetchone()
    conn.close()
    
    if password_data:
        decrypted_password = decrypt_password(password_data[2])
        return render_template('view_password.html',
                             service_name=password_data[0],
                             username=password_data[1],
                             password=decrypted_password,
                             notes=password_data[3])
    else:
        flash('Password not found')
        return redirect(url_for('dashboard'))

@app.route('/delete_password/<int:password_id>')
def delete_password(password_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('vault.db')
    c = conn.cursor()
    c.execute('DELETE FROM passwords WHERE id = ? AND user_id = ?', 
              (password_id, session['user_id']))
    conn.commit()
    conn.close()
    
    flash('Password deleted successfully!')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)