import argparse

from rich.console import Console

from .registry import CHECKS
from .report import save_html_report
from .report import save_json_report
from .engine import AuditEngine
from .utils import banner, display_result, display_summary

console = Console()

def main():
    banner()


    parser = argparse.ArgumentParser(
        description="GuardCLI Linux Security Audit Tool"
    )

    parser.add_argument(
        "--quick",
        action="store_true",
        help="Display only the summary."
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Generate a JSON report."
    )

    parser.add_argument(
        "--list-checks",
        action="store_true",
        help="List all available audit checks."
    )

    parser.add_argument(
        "--check",
        metavar="ID",
        help="Run a single audit check."
    )

    parser.add_argument(
        "--html",
        action="store_true",
        help="Generate an HTML report."
    )

    args = parser.parse_args()

    if args.check:

        selected = None

        for check_id, name, function in CHECKS:

            if check_id.upper() == args.check.upper():

                selected = (check_id, name, function)
                break

        if selected is None:

            console.print(
                f"[bold red]Unknown check:[/bold red] {args.check}"
            )

            return

        engine = AuditEngine()

        engine.run_check(selected[2])

        results = engine.get_results()

        for result in results:
            display_result(console, result)

        display_summary(console, results)

        if args.json:
            report = save_json_report(results)

            console.print(
                f"\n[green]JSON report saved:[/green] {report}"
            )

        return

    if args.list_checks:

        console.print("\n[bold cyan]Available Audit Checks[/bold cyan]\n")

        from rich.table import Table

        table = Table()

        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")

        for check_id, name, _ in CHECKS:
            table.add_row(check_id, name)

        console.print(table)
        return

    console.print("\n[green]Starting security audit...[/green]\n")

    engine = AuditEngine()
    
    for _, _, check in CHECKS:
        engine.run_check(check)

    results = engine.get_results()

    if not args.quick:
        for result in results:
            display_result(console, result)
   

    display_summary(console, results)
    

    if args.json:
        report = save_json_report(results)
        console.print(
            f"\n[green]JSON report saved:[/green] {report}"
        )

    if args.html:

        report = save_html_report(results)

        console.print(
            f"\n[green]HTML report saved:[/green] {report}"
        )

if __name__ == "__main__":
    main()
