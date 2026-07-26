"""
GuardCLI - Linux Personal OPSEC Audit Tool
Copyright (c) 2026 Rinshad0x

Licensed under the MIT License.
See LICENSE for details.
"""


import pwd


def run():

    findings = []
    issues = []

    users = pwd.getpwall()

    uid_zero_count = 0

    for user in users:

        findings.append({
            "User": user.pw_name,
            "UID": user.pw_uid,
            "Shell": user.pw_shell
        })

        if user.pw_uid == 0:
            uid_zero_count += 1

    if uid_zero_count > 1:
        issues.append(
            f"Found {uid_zero_count} users with UID 0."
        )

    score = max(0, 10 - len(issues) * 5)

    return {
        "id": "USER001",
        "category": "Users",
        "name": "User Account Audit",
        "severity": "Medium" if issues else "Low",
        "status": "WARNING" if issues else "PASS",
        "score": score,
        "issues": issues,
        "recommendation": (
            "Review privileged accounts and remove unnecessary UID 0 users."
            if issues
            else "No action required."
        ),
        "data": findings
    }
