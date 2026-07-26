"""
GuardCLI - Linux Personal OPSEC Audit Tool
Copyright (c) 2026 Rinshad0x

Licensed under the MIT License.
See LICENSE for details.
"""


from pathlib import Path
import os


SEARCH_DIRS = [
    "/etc",
    "/usr/local/bin",
    "/opt",
    str(Path.home()),
]

EXCLUDED_DIRS = (
    ".cache",
    ".local/share/Trash",
    ".mozilla",
    ".config/google-chrome",
    ".config/chromium",
    ".npm",
    ".cargo",
    "__pycache__",
    ".git",
)

HIGH_RISK = (
    ".service",
    ".conf",
    ".sh",
    ".bash",
    ".zsh",
)

MEDIUM_RISK = (
    ".py",
    ".pl",
    ".rb",
    ".php",
    ".js",
    ".c",
    ".cpp",
)

def run():

    findings = []
    issues = []

    for base in SEARCH_DIRS:

        base = Path(base)

        if not base.exists():
            continue

        for root, dirs, files in os.walk(base):

            for file in files:

                path = Path(root) / file

                path_str = str(path)

                if any(excluded in path_str for excluded in EXCLUDED_DIRS):
                    continue

                try:

                    mode = path.stat().st_mode

                    

                    if mode & 0o002:

                        severity = "Low"

                        suffix = path.suffix.lower()

                        # Executable files are always High risk
                        if os.access(path, os.X_OK):
                            severity = "High"

                        elif suffix in HIGH_RISK:
                            severity = "High"

                        elif suffix in MEDIUM_RISK:
                            severity = "Medium"

                        findings.append({
                            "Path": str(path),
                            "Permission": oct(mode & 0o777),
                            "Severity": severity,
                        })

                        issues.append(
                            f"World-writable file: {path}"
                        )

                except (
                    PermissionError,
                    FileNotFoundError,
                    OSError,
                ):
                    continue

    deduction = 0

    for item in findings:

        if item["Severity"] == "High":
            deduction += 3

        elif item["Severity"] == "Medium":
            deduction += 2

        else:
            deduction += 1

    score = max(0, 10 - deduction)

    if any(f["Severity"] == "High" for f in findings):
        severity = "High"

    elif any(f["Severity"] == "Medium" for f in findings):
        severity = "Medium"

    else:
        severity = "Low"
            
    findings = findings[:25]
    issues = issues[:25]        

    return {
        "id": "WW001",
        "category": "Filesystem",
        "name": "World Writable File Audit",
        "severity": severity,
        "status": "WARNING" if findings else "PASS",
        "score": score,
        "issues": issues,
        "recommendation": (
            "Review world-writable files and remove unnecessary write permissions (e.g. chmod o-w <file>)."
            if findings
            else "No action required."
        ),
        "data": findings,
    }
