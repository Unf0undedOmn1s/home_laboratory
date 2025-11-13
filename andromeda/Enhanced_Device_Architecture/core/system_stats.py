import psutil, time

def get_system_stats():
    return {
        'cpu': psutil.cpu_percent(interval=0.5),
        'memory': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('/').percent,
        'uptime': time.strftime("%H:%M:%S", time.gmtime(time.time() - psutil.boot_time()))
    }