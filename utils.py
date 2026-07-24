from rich.console import Console
from rich.panel import Panel
from rich import box

console = Console()

def banner():
    console.print(
        Panel.fit(
            "[bold cyan]Personal OPSEC Audit Tool[/bold cyan]\n"
            "[green]Version 1.0[/green]\n"
            "[yellow]by Rinshad0x[/yellow]",
            box=box.DOUBLE,
        )
    )
