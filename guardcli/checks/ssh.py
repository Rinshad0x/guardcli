from pathlib import Path
import os
import stat


def run():
    ssh_dir = Path.home() / ".ssh"

    issues = []
    data = []

    if not ssh_dir.exists():
        return {
            "id": "SSH001",
            "name": "SSH Key Audit",
            "severity": "Low",
            "status": "PASS",
            "score": 10,
            "issues": [],
            "recommendation": "",
            "data": ["No SSH directory found."]
        }

    for file in ssh_dir.iterdir():

        if file.is_file():

            permissions = stat.filemode(file.stat().st_mode)

            data.append({
                "file": file.name,
                "permissions": permissions
            })

            if file.name.startswith("id_") and not file.name.endswith(".pub"):

                mode = oct(file.stat().st_mode & 0o777)

                if mode != "0o600":
                    issues.append(
                        f"{file.name} has permissions {mode} (expected 600)"
                    )

    return {
        "id": "SSH001",
        "category": "Authentication",
        "name" : "SSH Key Audit",
        "severity": "Medium" if issues else "Low",
        "status": "WARNING" if issues else "PASS",
        "score": max(0, 10 - len(issues) * 2),
        "issues": issues,
        "recommendation": (
            "Run chmod 600 on private SSH keys."
            if issues
            else "No action required."
    ),
        "data": data
    }
