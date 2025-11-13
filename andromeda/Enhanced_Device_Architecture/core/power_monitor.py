import time
import os
import psutil

def read_rapl_energy():
    """Try to read CPU package energy via Intel RAPL."""
    base_path = "/sys/class/powercap"
    try:
        # Find the first RAPL device
        rapl_path = None
        for entry in os.listdir(base_path):
            if entry.startswith("intel-rapl:"):
                rapl_path = os.path.join(base_path, entry, "energy_uj")
                break
        if not rapl_path or not os.path.exists(rapl_path):
            raise FileNotFoundError("No RAPL device found")

        with open(rapl_path, "r") as f:
            start = int(f.read())

        time.sleep(1)

        with open(rapl_path, "r") as f:
            end = int(f.read())

        energy_joules = (end - start) / 1_000_000.0  # µJ → J
        watts = round(energy_joules / 1.0, 2)

        return {
            "power": watts,
            "voltage": 230,
            "current": round(watts / 230, 3),
            "source": "intel_rapl"
        }

    except Exception as e:
        raise RuntimeError(f"RAPL unavailable: {e}")

def read_psutil_fallback():
    """Fallback using psutil for approximate CPU load + temperature."""
    cpu_usage = psutil.cpu_percent(interval=1)
    temps = psutil.sensors_temperatures()
    cpu_temp = None
    if temps:
        for name, entries in temps.items():
            if entries:
                cpu_temp = entries[0].current
                break

    return {
        "power": round(cpu_usage * 1.5, 2),  # rough estimate
        "voltage": 230,
        "current": round((cpu_usage * 1.5) / 230, 3),
        "cpu_temp": cpu_temp or "N/A",
        "source": "psutil_fallback"
    }

def get_power_data():
    """Main entry: try RAPL first, then psutil."""
    try:
        return read_rapl_energy()
    except Exception:
        return read_psutil_fallback()