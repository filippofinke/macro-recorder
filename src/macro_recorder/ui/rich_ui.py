import time

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from macro_recorder.models.recording import Recording


class RichUI:
    def __init__(self):
        self.console = Console()

    def header(self) -> None:
        self.console.print(Panel.fit(
            "[bold magenta]MACRO RECORDER[/]",
            border_style="magenta"
        ))

    def countdown(self, seconds: int) -> None:
        with self.console.status("[bold yellow]Get ready...[/]") as status:
            for i in range(seconds, 0, -1):
                status.update(f"[bold yellow]Starting in {i}...[/]")
                time.sleep(1)

    def info(self, message: str) -> None:
        self.console.print(f"[cyan][INFO] {message}[/]")

    def success(self, message: str) -> None:
        self.console.print(f"[green][OK] {message}[/]")

    def warning(self, message: str) -> None:
        self.console.print(f"[yellow][WARN] {message}[/]")

    def error(self, message: str) -> None:
        self.console.print(f"[red][ERROR] {message}[/]")

    def show_recording_stats(self, recording: Recording) -> None:
        meta = recording.metadata
        table = Table(title=f"Stats: {meta.name}", border_style="blue")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")
        table.add_row("Duration", f"{meta.duration:.2f}s")
        table.add_row("Total Events", str(meta.event_count))
        table.add_row("  Moves", str(meta.move_count))
        table.add_row("  Clicks", str(meta.click_count))
        table.add_row("  Scrolls", str(meta.scroll_count))
        self.console.print(table)

    def show_shortcuts(self) -> None:
        table = Table(border_style="dim")
        table.add_column("Key", style="bold cyan")
        table.add_column("Action", style="white")
        table.add_row("Cmd+R", "Stop recording")
        table.add_row("Cmd+Space", "Pause/Resume")
        table.add_row("ESC", "Exit playback")
        self.console.print(table)
