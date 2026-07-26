import os

SENSITIVE_KEYWORDS = [
    "PASSWORD",
    "PASS",
    "SECRET",
    "TOKEN",
    "API_KEY",
    "APIKEY",
    "ACCESS_KEY",
    "PRIVATE_KEY",
    "AWS",
    "OPENAI",
    "GITHUB",
]


def run():
    findings = []

    for key in os.environ:
        upper = key.upper()

        if any(keyword in upper for keyword in SENSITIVE_KEYWORDS):
            findings.append({
                "Variable": key
            })

    issues = []

    if findings:
        issues.append("Sensitive environment variables detected.")

    score = max(0, 10 - len(findings))

    return {
        "id": "ENV001",
        "category": "Environment",
        "name": "Environment Variables",
        "severity": "Medium" if findings else "Low",
        "status": "WARNING" if findings else "PASS",
        "score": score,
        "issues": issues,
        "recommendation": (
            "Avoid storing long-lived secrets in environment variables."
            if findings
            else "No action required."
        ),
        "data": findings
    }
