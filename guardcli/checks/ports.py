import psutil


def run():
    ports = []

    for conn in psutil.net_connections(kind="inet"):

        if conn.status != psutil.CONN_LISTEN:
            continue

        process = "Unknown"

        if conn.pid:
            try:
                process = psutil.Process(conn.pid).name()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                process = "Unknown"

        ports.append({
            "port": conn.laddr.port,
            "ip": conn.laddr.ip,
            "process": process
        })

    issues = []

    risky_ports = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        139: "NetBIOS",
        143: "IMAP",
        443: "HTTPS",
        445: "SMB",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        5900: "VNC",
        8080: "HTTP Proxy"
    }

    for port in ports:
        if port["port"] in risky_ports:
            issues.append(
                f"Port {port['port']} ({risky_ports[port['port']]}) is listening."
            )

    score = max(0, 10 - len(issues) * 2)

    return {
        "id": "PORT001",
        "category": "Network",
        "name": "Open Ports",
        "severity": "Medium" if issues else "Low",
        "status": "WARNING" if issues else "PASS",
        "score": score,
        "issues": issues,
        "recommendation": (
            "Close unnecessary services and verify exposed ports."
            if issues else
            "No action required."
        ),
        "data": ports
    }
