from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich import box

console = Console()

def banner():
    console.print(
        Panel.fit(
            "[bold bright_cyan]GuardCLI[/bold bright_cyan]\n"
            "[green]A Personal OPSEC Audit Tool for Linux[/green]\n\n"
            "[yellow]Analyze • Detect • Improve[/yellow]\n"
            "[white]Version 1.0[/white]\n"
            "[dim]by Rinshad0x[/dim]",
            box=box.DOUBLE,
        )
    )


def display_result(console, result):
    """Display any audit result in a consistent format."""

    console.rule(f"[bold cyan]{result['name']}[/bold cyan]")

    console.print(f"[bold]Status:[/bold] {result['status']}")
    console.print(f"[bold]Severity:[/bold] {result.get('severity', 'N/A')}")
    console.print(f"[bold]Score:[/bold] {result['score']}")

    data = result.get("data")

    if data:
        # Dictionary (System Information)
        if isinstance(data, dict):
            table = Table(show_header=True)
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="green")

            for key, value in data.items():
                table.add_row(str(key), str(value))

            console.print(table)

        # List of dictionaries (Ports, SSH files, ...)
        elif isinstance(data, list):

            if len(data) > 0 and isinstance(data[0], dict):

                table = Table(show_header=True)

                for column in data[0].keys():
                    table.add_column(column.capitalize())

                for row in data:
                    table.add_row(*(str(v) for v in row.values()))

                console.print(table)

            # List of strings
            else:
                for item in data:
                    console.print(f"• {item}")

    if result["issues"]:
        console.print("\n[bold yellow]Issues[/bold yellow]")

        for issue in result["issues"]:
            console.print(f"⚠ {issue}")

    if result["recommendation"]:
        console.print(
            f"\n[bold green]Recommendation:[/bold green] {result['recommendation']}"
        )

    console.print()

def display_summary(console, results):
    console.rule("[bold green]GuardCLI Summary[/bold green]")

    total_score = sum(result["score"] for result in results)
    max_score = len(results) * 10

    passed = sum(1 for result in results if result["status"] == "PASS")
    warnings = sum(1 for result in results if result["status"] != "PASS")

    percentage = (total_score / max_score) * 100 if max_score else 0

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

    console.print(f"[bold cyan]Overall Score:[/bold cyan] {total_score}/{max_score}")
    console.print(f"[bold cyan]Grade:[/bold cyan] {grade}")
    console.print(f"[bold cyan]Risk Level:[/bold cyan] {risk}")
    console.print(f"[bold cyan]Checks Passed:[/bold cyan] {passed}")
    console.print(f"[bold cyan]Warnings:[/bold cyan] {warnings}")
