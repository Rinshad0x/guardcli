from rich.console import Console
from rich.table import Table

from utils import banner
from checks.system import system_info

console = Console()


def display_system_info(result):
    table = Table(title=result["name"])

    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    for key, value in result["data"].items():
        table.add_row(key, str(value))

    console.print(table)


def main():
    banner()

    console.print("\n[green]Starting security audit...[/green]\n")

    result = system_info()

    display_system_info(result)


if __name__ == "__main__":
    main()
