"""
GuardCLI - Linux Personal OPSEC Audit Tool
Copyright (c) 2026 Rinshad0x

Licensed under the MIT License.
See LICENSE for details.
"""


from pathlib import Path
import re

# Pattern -> Severity label
PATTERNS = [
    (
        re.compile(r"authorization:\s*bearer", re.IGNORECASE),
        "Bearer token detected",
        "High"
    ),
    (
        re.compile(r"password\s*=", re.IGNORECASE),
        "Password assignment detected",
        "High"
    ),
    (
        re.compile(r"export\s+.*api[_-]?key", re.IGNORECASE),
        "API key exported",
        "Medium"
    ),
    (
        re.compile(r"mysql\s+.*-p\S+", re.IGNORECASE),
        "Password passed to MySQL command",
        "High"
    ),
    (
        re.compile(r"curl.*authorization", re.IGNORECASE),
        "Authorization header in curl command",
        "Medium"
    ),
    (
        re.compile(r"gh auth login", re.IGNORECASE),
        "GitHub authentication command",
        "Low"
    ),
    (
        re.compile(r"aws configure", re.IGNORECASE),
        "AWS CLI configuration",
        "Low"
    ),
]

HISTORY_FILES = [
    ".bash_history",
    ".zsh_history",
]


def run():
    findings = []
    issues = []

    home = Path.home()

    for history_file in HISTORY_FILES:
        path = home / history_file

        if not path.exists():
            continue

        try:
            with open(path, "r", errors="ignore") as f:
                for line_number, line in enumerate(f, start=1):
                    lower = line.lower()

                    for regex, description, severity in PATTERNS:

                         if regex.search(line):

                             findings.append({
                                 "File": history_file,
                                 "Line": line_number,
                                 "Issue": description,
                                 "Severity": severity
                             })

                             break

        except Exception:
            continue

    if findings:
        issues.append("Potentially sensitive commands were found in shell history.")

    high = sum(
        1 for f in findings
        if f["Severity"] == "High"
    )

    medium = sum(
        1 for f in findings
        if f["Severity"] == "Medium"
    )

    low = sum(
        1 for f in findings
        if f["Severity"] == "Low"
    )

    deduction = (
        high * 3 +
        medium * 2 +
        low
    )

    score = max(0, 10 - deduction)

    if high > 0:
        severity = "High"
    elif medium > 0:
        severity = "Medium"
    elif low > 0:
        severity = "Low"
    else:
        severity = "Low"

    return {
        "id": "HIST001",
        "category": "Shell",
        "name": "Shell History Audit",
        "severity": severity,
        "status": "WARNING" if findings else "PASS",
        "score": score,
        "issues": issues,
        "recommendation": (
            "Avoid entering passwords, tokens, or secrets directly into shell commands."
            if findings
            else "No action required."
        ),
        "data": findings
    }
