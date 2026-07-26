"""
GuardCLI - Linux Personal OPSEC Audit Tool
Copyright (c) 2026 Rinshad0x

Licensed under the MIT License.
See LICENSE for details.
"""

from .checks import ssh_config
from .checks import world_writable
from .checks import (
    system,
    users,
    ports,
    firewall,
    processes,
    ssh,
    env,
    permissions,
    history,
    suid,
    cron,
)

CHECKS = [
    ("SYS001", "System Information", system.run),
    ("USR001", "User Account Audit", users.run),
    ("PORT001", "Open Ports", ports.run),
    ("FW001", "Firewall Audit", firewall.run),
    ("PROC001", "Running Process Audit", processes.run),
    ("SSH001", "SSH Key Audit", ssh.run),
    ("ENV001", "Environment Variables", env.run),
    ("PERM001", "File Permission Audit", permissions.run),
    ("HIST001", "Shell History Audit", history.run),
    ("SUID001", "SUID Binary Audit", suid.run),
    ("CRON001", "Cron Job Audit", cron.run),
    ("WW001", "World Writable File Audit", world_writable.run),
    ("SSHD001", "SSH Configuration Audit", ssh_config.run),
]
