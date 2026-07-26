"""
GuardCLI - Linux Personal OPSEC Audit Tool
Copyright (c) 2026 Rinshad0x

Licensed under the MIT License.
See LICENSE for details.
"""


import json
from pathlib import Path
from datetime import datetime

from jinja2 import Environment
from jinja2 import FileSystemLoader

def save_json_report(results):

    reports = Path("reports")
    reports.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    total_score = sum(r["score"] for r in results)
    maximum = len(results) * 10

    percentage = (total_score / maximum) * 100 if maximum else 0

    if percentage >= 90:
        grade = "A"
        risk = "LOW"

    elif percentage >= 75:
        grade = "B"
        risk = "LOW"

    elif percentage >= 60:
        grade = "C"
        risk = "MEDIUM"

    elif percentage >= 40:
        grade = "D"
        risk = "HIGH"

    else:
        grade = "F"
        risk = "CRITICAL"

    filename = reports / f"GuardCLI_Report_{timestamp}.json"

    report = {
        "tool": "GuardCLI",
        "version": "1.0",
        "generated": timestamp,
        "summary": {
            "score": total_score,
            "maximum": maximum
        },
        "checks": results
    }

    with open(filename, "w") as f:
        json.dump(report, f, indent=4)

    return filename

def save_html_report(results):

    reports = Path("reports")
    reports.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    total_score = sum(r["score"] for r in results)
    maximum = len(results) * 10

    percentage = (total_score / maximum) * 100 if maximum else 0

    if percentage >= 90:
        grade = "A"
        risk = "LOW"

    elif percentage >= 75:
        grade = "B"
        risk = "LOW"

    elif percentage >= 60:
        grade = "C"
        risk = "MEDIUM"

    elif percentage >= 40:
        grade = "D"
        risk = "HIGH"

    else:
        grade = "F"
        risk = "CRITICAL"

    env = Environment(
        loader=FileSystemLoader("guardcli/templates")
    )

    template = env.get_template("report.html")

    html = template.render(

        generated=timestamp,

        score=total_score,

        maximum=maximum,

        grade=grade,

        risk=risk,

        checks=results

    )

    filename = reports / f"GuardCLI_Report_{timestamp}.html"

    with open(filename,"w") as f:

        f.write(html)

    return filename
