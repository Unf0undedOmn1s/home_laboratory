from flask import Flask, render_template, jsonify, request, Response
from core.system_stats import get_system_stats
from core.network_scan import scan_network
from core.packet_analyzer import capture_packets
from core.power_monitor import get_power_data
from core.alert_manager import get_alerts
from core.alert_bot import send_telegram_alert

# User credentials
USERNAME = "andromeda"
PASSWORD = "trobomalakas02"


app = Flask(__name__)

from functools import wraps

def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response(
        'Authentication required.', 401,
        {'WWW-Authenticate': 'Basic realm="HomeLab Dashboard"'}
    )

# AUTH Function/User Authentication System
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
@requires_auth
def index():
    return render_template('index.html', title="Dashboard")

@app.route('/system')
@requires_auth
def system():
    return render_template('system.html', title="System")

@app.route('/network')
@requires_auth
def network():
    devices = scan_network()
    return render_template('network.html', title="Network", devices=devices)

@app.route('/packets')
@requires_auth
def packets():
    packets = capture_packets(15)
    return render_template('packets.html', title="Packet Analyzer", packets=packets)

@app.route('/alerts')
@requires_auth
def alerts():
    return render_template('alerts.html', title="Alerts", alerts=get_alerts())

@app.route('/power_monitor')
@requires_auth
def power_monitor_page():
    return render_template('power.html', title="Power Monitor")

@app.route('/system/data')
@requires_auth
def system_data():
    return jsonify(get_system_stats())

@app.route('/power')
@requires_auth
def power_api():
    try:
        return jsonify(get_power_data())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/test_alert', methods=['POST'])
def test_alert():
    try:
        send_telegram_alert("🛰️ Test alert sent from your Andromeda dashboard!", "info")
        return jsonify({"status": "success", "message": "Telegram alert sent!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)