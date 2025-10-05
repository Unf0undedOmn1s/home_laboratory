from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
from datetime import datetime
import os
import json
from werkzeug.utils import secure_filename
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# In-memory storage
passwords_data = []
logs = []

def log_event(message):
    """Add event to logs"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logs.append({"timestamp": timestamp, "message": message})
    print(f"[{timestamp}] {message}")

log_event("Password Vault Manager started")

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_csv():
    """Handle CSV file upload"""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "Only CSV files are allowed"}), 400
    
    try:
        # Read CSV
        df = pd.read_csv(file)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Convert to list of dicts
        new_entries = df.to_dict('records')
        
        # Add to existing data
        passwords_data.extend(new_entries)
        
        log_event(f"Uploaded CSV: {file.filename} ({len(new_entries)} entries)")
        
        return jsonify({
            "success": True,
            "message": f"Loaded {len(new_entries)} entries",
            "total": len(passwords_data)
        })
    
    except Exception as e:
        log_event(f"Error uploading CSV: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/passwords', methods=['GET'])
def get_passwords():
    """Get all passwords with optional search"""
    try:
        search_query = request.args.get('search', '').lower()
        
        if not search_query:
            filtered = passwords_data
        else:
            filtered = []
            for entry in passwords_data:
                try:
                    # Convert all values to string and search
                    if any(search_query in str(value).lower() for value in entry.values() if value is not None):
                        filtered.append(entry)
                except Exception as e:
                    continue
            log_event(f"Search performed: '{search_query}' ({len(filtered)} results)")
        
        # Clean the data - ensure all values are JSON serializable
        clean_data = []
        for entry in filtered:
            clean_entry = {}
            for key, value in entry.items():
                # Handle NaN, None, and other non-serializable values
                if pd.isna(value) or value is None:
                    clean_entry[key] = ""
                else:
                    clean_entry[key] = str(value)
            clean_data.append(clean_entry)
        
        return jsonify({
            "data": clean_data,
            "total": len(passwords_data),
            "filtered": len(clean_data)
        })
    except Exception as e:
        log_event(f"Error in get_passwords: {str(e)}")
        return jsonify({
            "data": [],
            "total": 0,
            "filtered": 0,
            "error": str(e)
        }), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get all logs"""
    return jsonify({"logs": logs})

@app.route('/api/export', methods=['GET'])
def export_data():
    """Export data as CSV"""
    if not passwords_data:
        return jsonify({"error": "No data to export"}), 400
    
    try:
        df = pd.DataFrame(passwords_data)
        export_path = os.path.join(app.config['UPLOAD_FOLDER'], 'export.csv')
        df.to_csv(export_path, index=False)
        
        log_event("Data exported")
        return send_file(export_path, as_attachment=True, download_name='vault_export.csv')
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/export-logs', methods=['GET'])
def export_logs():
    """Export logs as text file"""
    try:
        export_path = os.path.join(app.config['UPLOAD_FOLDER'], 'logs.txt')
        with open(export_path, 'w') as f:
            for log in logs:
                f.write(f"[{log['timestamp']}] {log['message']}\n")
        
        log_event("Logs exported")
        return send_file(export_path, as_attachment=True, download_name='vault_logs.txt')
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/clear', methods=['POST'])
def clear_data():
    """Clear all password data"""
    global passwords_data
    passwords_data = []
    log_event("All data cleared")
    return jsonify({"success": True, "message": "All data cleared"})

if __name__ == '__main__':
    # Run on all network interfaces so it's accessible on local network
    app.run(host='0.0.0.0', port=5000, debug=True)