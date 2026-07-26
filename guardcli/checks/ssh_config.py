"""
GuardCLI - Linux Personal OPSEC Audit Tool
Copyright (c) 2026 Rinshad0x

Licensed under the MIT License.
See LICENSE for details.
"""


from pathlib import Path


CONFIG_FILE = Path("/etc/ssh/sshd_config")


SECURE_SETTINGS = {
    "PermitRootLogin": "no",
    "PasswordAuthentication": "no",
    "PermitEmptyPasswords": "no",
    "PubkeyAuthentication": "yes",
    "X11Forwarding": "no",
}

DEFAULTS = {
    "PermitRootLogin": "prohibit-password",
    "PasswordAuthentication": "yes",
    "PermitEmptyPasswords": "no",
    "PubkeyAuthentication": "yes",
    "X11Forwarding": "yes",
}

def run():

    findings = []
    issues = []

    if not CONFIG_FILE.exists():

        return {
            "id": "SSHD001",
            "category": "SSH",
            "name": "SSH Configuration Audit",
            "severity": "Low",
            "status": "PASS",
            "score": 10,
            "issues": [],
            "recommendation": "OpenSSH server is not installed.",
            "data": [],
        }

    settings = {}

    with open(CONFIG_FILE, "r", errors="ignore") as f:

        for line in f:

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split()

            if len(parts) >= 2:
                settings[parts[0]] = parts[1]

    score = 10

    highest_severity = "Low"

    for key, expected in SECURE_SETTINGS.items():

        actual = settings.get(key, DEFAULTS[key])

        severity = "Low"

        is_secure = False

        if key == "PermitRootLogin":

            if actual.lower() in (
                "no",
                "prohibit-password",
                "forced-commands-only",
            ):
                is_secure = True

        else:

            if actual.lower() == expected.lower():
                is_secure = True


        if not is_secure:

            if key == "PermitEmptyPasswords":
                severity = "Critical"
                score -= 5

            elif key == "PermitRootLogin":
                severity = "High"
                score -= 3

            elif key == "PasswordAuthentication":
                severity = "Medium"
                score -= 2

            elif key == "X11Forwarding":
                severity = "Low"
                score -= 1

            issues.append(
                f"{key} = {actual} (recommended: {expected})"
            )  
             

        findings.append({
            "Setting": key,
            "Current": actual,
            "Recommended": expected,
            "Severity": severity,
        })

        levels = {
            "Low": 1,
            "Medium": 2,
            "High": 3,
            "Critical": 4,
        }

        if levels[severity] > levels[highest_severity]:
            highest_severity = severity

    score = max(0, score)

    return {
        "id": "SSHD001",
        "category": "SSH",
        "name": "SSH Configuration Audit",
        "severity": highest_severity,
        "status": "WARNING" if issues else "PASS",
        "score": score,
        "issues": issues,
        "recommendation": (
            "Review insecure SSH settings and apply the recommended values."
            if issues
            else "SSH configuration follows the recommended baseline."
        ),
        "data": findings,
    }
