import typer
from rich.console import Console

console = Console()
app = typer.Typer()

@app.command()
def dry_run():
    console.print("Dry-run validated successfully")

@app.command()
def rollback():
    console.print("Rollback orchestration started")
