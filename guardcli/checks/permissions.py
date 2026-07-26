from pathlib import Path
import stat

FILES_TO_CHECK = {
    ".bash_history": "600",
    ".zsh_history": "600",
    ".git-credentials": "600",
    ".env": "600",
    ".netrc": "600",
}


def run():
    home = Path.home()

    findings = []
    issues = []

    for filename, expected in FILES_TO_CHECK.items():

        file = home / filename

        if not file.exists():
            continue

        mode = oct(file.stat().st_mode & 0o777)[2:]

        findings.append({
            "File": filename,
            "Permission": mode,
            "Expected": expected
        })

        if mode != expected:
            issues.append(
                f"{filename} has permission {mode} (expected {expected})"
            )

    score = max(0, 10 - len(issues) * 2)

    return {
        "id": "PERM001",
        "category": "Filesystem",
        "name": "File Permission Audit",
        "severity": "Medium" if issues else "Low",
        "status": "WARNING" if issues else "PASS",
        "score": score,
        "issues": issues,
        "recommendation": (
            "Run chmod 600 on sensitive files."
            if issues
            else "No action required."
        ),
        "data": findings
    }
