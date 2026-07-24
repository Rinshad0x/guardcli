import platform
import socket
import getpass


def system_info():
    info = {
        "Username": getpass.getuser(),
        "Hostname": socket.gethostname(),
        "OS": platform.system(),
        "Release": platform.release(),
        "Machine": platform.machine(),
        "Processor": platform.processor() or "Unknown"
    }

    return {
        "name": "System Information",
        "status": "PASS",
        "score": 10,
        "issues": [],
        "recommendation": "",
        "data": info
    }
