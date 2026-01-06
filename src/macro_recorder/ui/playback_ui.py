from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn, TaskID

from macro_recorder.models.recording import Recording
from macro_recorder.observers.playback_observer import PlaybackObserver


class PlaybackUI(PlaybackObserver):
    def __init__(self, console: Console):
        self.console = console
        self._progress: Progress | None = None
        self._task_id: TaskID | None = None
        self._iteration = 0
        self._total_iterations = 0

    def on_playback_start(self, recording: Recording, total_iterations: int) -> None:
        self._total_iterations = total_iterations
        self._progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            console=self.console
        )
        self._progress.start()

    def on_iteration_start(self, iteration: int, total: int) -> None:
        self._iteration = iteration
        if self._progress and self._task_id is not None:
            self._progress.remove_task(self._task_id)
        if self._progress:
            desc = f"Iteration {iteration}" + (f"/{total}" if total > 0 else "/inf")
            self._task_id = self._progress.add_task(desc, total=100)

    def on_event_played(self, index: int, total: int) -> None:
        if self._progress and self._task_id is not None:
            self._progress.update(self._task_id, completed=(index / total) * 100)

    def on_playback_complete(self) -> None:
        if self._progress:
            self._progress.stop()
        self.console.print("[green]Playback complete![/]")

    def on_playback_pause(self) -> None:
        self.console.print("[yellow]Paused - Press Cmd+Space to resume[/]")

    def on_playback_resume(self) -> None:
        self.console.print("[green]Resumed[/]")
