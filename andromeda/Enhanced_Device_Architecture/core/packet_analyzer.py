from scapy.all import sniff
import datetime

def capture_packets(count=10):
    packets = sniff(count=count)
    data = []
    for p in packets:
        src = getattr(p[0][1], 'src', 'N/A')
        dst = getattr(p[0][1], 'dst', 'N/A')
        proto = getattr(p, 'proto', 'N/A')
        data.append({
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "src": src,
            "dst": dst,
            "proto": proto
        })
    return data