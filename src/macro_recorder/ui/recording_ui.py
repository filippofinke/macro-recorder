import time

from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.text import Text

from macro_recorder.models.mouse_event import MouseEvent
from macro_recorder.models.event_type import EventType
from macro_recorder.models.recording_metadata import RecordingMetadata
from macro_recorder.observers.recording_observer import RecordingObserver


class RecordingUI(RecordingObserver):
    def __init__(self, console: Console):
        self.console = console
        self.start_time = 0.0
        self.event_count = 0
        self.click_count = 0
        self.scroll_count = 0
        self._live: Live | None = None
        self._running = False

    def _build_panel(self) -> Panel:
        elapsed = time.time() - self.start_time
        content = Text()
        content.append(f"Duration: {elapsed:06.2f}s\n", style="white")
        content.append(f"Events:   {self.event_count:,}\n", style="white")
        content.append(f"Clicks:   {self.click_count}  |  Scrolls: {self.scroll_count}", style="dim")
        return Panel(content, title="[bold red]Recording[/]", border_style="red")

    def on_start(self) -> None:
        self.start_time = time.time()
        self.event_count = 0
        self.click_count = 0
        self.scroll_count = 0
        self._running = True
        self._live = Live(self._build_panel(), console=self.console, refresh_per_second=10)
        self._live.start()

    def on_event(self, event: MouseEvent) -> None:
        self.event_count += 1
        if event.event_type == EventType.CLICK and event.pressed:
            self.click_count += 1
        elif event.event_type == EventType.SCROLL:
            self.scroll_count += 1
        if self._live:
            self._live.update(self._build_panel())

    def on_stop(self, metadata: RecordingMetadata) -> None:
        self._running = False
        if self._live:
            self._live.stop()
        self.console.print(f"[green]Recording saved: {metadata.name}[/]")

    def on_pause(self) -> None:
        if self._live:
            self._live.update(Panel(
                Text("PAUSED - Press Cmd+Space to resume", style="yellow"),
                title="[bold yellow]Paused[/]",
                border_style="yellow"
            ))

    def on_resume(self) -> None:
        if self._live:
            self._live.update(self._build_panel())
