import socket
from concurrent.futures import ThreadPoolExecutor

import psutil

COMMON_PORTS = {
    20: "FTP-data", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 139: "NetBIOS", 143: "IMAP", 443: "HTTPS",
    445: "SMB", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
    5000: "Dev server", 8000: "Dev server", 8080: "HTTP-alt",
    8501: "Streamlit", 27017: "MongoDB",
}


def scan_open_ports(host="127.0.0.1", ports=None, timeout=0.3):
    """Try connecting to each port; if the connection succeeds, it's open."""
    ports = ports or list(COMMON_PORTS.keys())

    def check(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            is_open = sock.connect_ex((host, port)) == 0
            return port, is_open

    open_ports = []
    with ThreadPoolExecutor(max_workers=20) as pool:
        for port, is_open in pool.map(check, ports):
            if is_open:
                open_ports.append((port, COMMON_PORTS.get(port, "Unknown")))

    return sorted(open_ports)


def get_system_stats():
    """Current CPU %, memory %, and disk usage % as plain numbers."""
    return {
        "cpu": psutil.cpu_percent(interval=0.5),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("C:\\").percent,
    }
