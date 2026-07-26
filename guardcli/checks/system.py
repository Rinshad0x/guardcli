"""
GuardCLI - Linux Personal OPSEC Audit Tool
Copyright (c) 2026 Rinshad0x

Licensed under the MIT License.
See LICENSE for details.
"""


import platform
import socket
import getpass


def run():
    info = {
        "Username": getpass.getuser(),
        "Hostname": socket.gethostname(),
        "OS": platform.system(),
        "Release": platform.release(),
        "Machine": platform.machine(),
        "Processor": platform.processor() or "Unknown",
    }

    return {
        "id": "SYS001",
        "category": "Host",
        "name" : "System Information",
        "severity": "Info",
        "status": "PASS",
        "score": 10,
        "issues": [],
        "recommendation": "No action required",
        "data": info,
    }
