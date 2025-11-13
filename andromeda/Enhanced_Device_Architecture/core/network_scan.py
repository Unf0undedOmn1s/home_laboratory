from scapy.all import ARP, Ether, srp

def scan_network(subnet="192.168.2.6/24"):
    arp = ARP(pdst=subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    result = srp(ether/arp, timeout=2, verbose=False)[0]
    devices = [{"ip": r.psrc, "mac": r.hwsrc} for s, r in result]
    return devices