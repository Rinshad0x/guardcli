"""
GuardCLI - Linux Personal OPSEC Audit Tool
Copyright (c) 2026 Rinshad0x

Licensed under the MIT License.
See LICENSE for details.
"""


from pathlib import Path

CRON_LOCATIONS = [
    "/etc/crontab",
    "/etc/cron.d",
    "/etc/cron.daily",
    "/etc/cron.hourly",
    "/etc/cron.weekly",
    "/etc/cron.monthly",
]


def run():

    findings = []
    issues = []

    for location in CRON_LOCATIONS:

        path = Path(location)

        if not path.exists():
            continue

        if path.is_file():

            findings.append({
                "Location": location,
                "Type": "File"
            })

            mode = oct(path.stat().st_mode & 0o777)[2:]

            if mode in ("666", "777"):
                issues.append(
                    f"{location} is world writable."
                )

        elif path.is_dir():

            findings.append({
                "Location": location,
                "Type": "Directory"
            })

            for item in path.iterdir():

                try:

                    mode = oct(item.stat().st_mode & 0o777)[2:]

                    if mode in ("666", "777"):

                        issues.append(
                            f"{item} is world writable."
                        )

                except Exception:
                    continue

    score = max(0, 10 - min(len(issues), 5) * 2)

    return {
        "id": "CRON001",
        "category": "Persistence",
        "name": "Cron Job Audit",
        "severity": "Medium" if issues else "Low",
        "status": "WARNING" if issues else "PASS",
        "score": score,
        "issues": issues,
        "recommendation": (
            "Review writable cron files and directories."
            if issues
            else "No action required."
        ),
        "data": findings
    }
