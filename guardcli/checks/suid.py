"""
GuardCLI - Linux Personal OPSEC Audit Tool
Copyright (c) 2026 Rinshad0x

Licensed under the MIT License.
See LICENSE for details.
"""


import subprocess


COMMON_SUID = {
    "/usr/bin/passwd",
    "/usr/bin/su",
    "/usr/bin/sudo",
    "/usr/bin/chfn",
    "/usr/bin/chsh",
    "/usr/bin/gpasswd",
    "/usr/bin/mount",
    "/usr/bin/umount",
    "/usr/bin/newgrp",
    "/usr/bin/pkexec",
}


def run():

    findings = []
    issues = []

    try:
        result = subprocess.run(
            ["find", "/", "-perm", "-4000", "-type", "f"],
            capture_output=True,
            text=True,
            stderr=subprocess.DEVNULL,
        )

        binaries = result.stdout.splitlines()

    except Exception:

        binaries = []

    for binary in binaries:

        findings.append({
            "Binary": binary
        })

        if binary not in COMMON_SUID:
            issues.append(
                f"Review uncommon SUID binary: {binary}"
            )

    score = max(0, 10 - min(len(issues), 5) * 2)

    return {
        "id": "SUID001",
        "category": "Privilege Escalation",
        "name": "SUID Binary Audit",
        "severity": "Medium" if issues else "Low",
        "status": "WARNING" if issues else "PASS",
        "score": score,
        "issues": issues,
        "recommendation": (
            "Review uncommon SUID binaries and remove the SUID bit if unnecessary."
            if issues
            else "No action required."
        ),
        "data": findings,
    }
