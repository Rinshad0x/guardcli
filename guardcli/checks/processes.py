"""
GuardCLI - Linux Personal OPSEC Audit Tool
Copyright (c) 2026 Rinshad0x

Licensed under the MIT License.
See LICENSE for details.
"""


import psutil
from pathlib import Path


SUSPICIOUS_PATHS = (
    "/tmp",
    "/var/tmp",
    "/dev/shm",
)

IMPORTANT = {
    "python",
    "python3",
    "ssh",
    "sshd",
    "docker",
    "dockerd",
    "nginx",
    "apache2",
    "httpd",
    "mysql",
    "mysqld",
    "postgres",
    "postgresql",
    "redis-server",
    "mongod",
    "node",
    "java",
    "php",
    "ruby",
    "perl",
}

def run():

    findings = []
    issues = set()

    for proc in psutil.process_iter(
        ["pid", "name", "exe", "username"]
    ):

        try:

            exe = proc.info["exe"] or ""
            name = (proc.info["name"] or "").lower()
            user = proc.info["username"] or "Unknown"

            is_important = (
                name in IMPORTANT
            )

            is_suspicious = any(
                exe.startswith(path)
                for path in SUSPICIOUS_PATHS
            )

            if is_important or is_suspicious:

                findings.append({
                    "PID": proc.info["pid"],
                    "Name": proc.info["name"],
                    "User": user,
                    "Executable": exe if exe else "Unknown",
                })

            for path in SUSPICIOUS_PATHS:

                if exe.startswith(path):

                    issues.add(
                        f"{proc.info['name']} is running from {path}"
                    )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    score = max(0, 10 - min(len(issues), 5) * 2)

    findings = findings[:30]
    
    issues = sorted(issues)

    return {
        "id": "PROC001",
        "category": "Processes",
        "name": "Running Process Audit",
        "severity": "Medium" if issues else "Low",
        "status": "WARNING" if issues else "PASS",
        "score": score,
        "issues": issues,
        "recommendation": (
            "Investigate processes running from temporary directories. Verify whether they are legitimate and terminate any unauthorized executables."
            if issues
            else "No action required."
        ),
        "data": findings,
    }
