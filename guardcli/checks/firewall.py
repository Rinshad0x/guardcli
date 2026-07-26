import subprocess


def command_exists(command):
    result = subprocess.run(
        ["which", command],
        capture_output=True,
        text=True
    )

    return result.returncode == 0


def run():

    findings = []
    issues = []

    firewalls = {
        "ufw": ["ufw", "status"],
        "iptables": ["iptables", "-L"],
        "nft": ["nft", "list", "ruleset"],
        "firewalld": ["firewall-cmd", "--state"],
    }

    active = False

    for name, command in firewalls.items():

        if not command_exists(command[0]):
            continue

        try:

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout.lower()

            enabled = False

            if name == "ufw":
                enabled = "status: active" in output

            elif name == "firewalld":
                enabled = "running" in output

            elif name == "iptables":
                enabled = len(output.strip()) > 0

            elif name == "nft":
                enabled = len(output.strip()) > 0

            findings.append({
                "Firewall": name,
                "Enabled": "Yes" if enabled else "No"
            })

            if enabled:
                active = True

        except Exception:
            continue

    if not active:
        issues.append("No active firewall detected.")

    score = 10 if active else 5

    return {
        "id": "FW001",
        "category": "Network",
        "name": "Firewall Audit",
        "severity": "Low" if active else "Medium",
        "status": "PASS" if active else "WARNING",
        "score": score,
        "issues": issues,
        "recommendation": (
            "Enable a firewall to reduce network exposure."
            if issues
            else "No action required."
        ),
        "data": findings
    }
