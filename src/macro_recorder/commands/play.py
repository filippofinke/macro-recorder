import sys
from pathlib import Path

from rich.console import Console

from macro_recorder.core import MacroPlayer
from macro_recorder.storage import StorageService
from macro_recorder.ui import RichUI, PlaybackUI


def cmd_play(args) -> None:
    if args.speed <= 0:
        Console().print("[red]Error: Speed must be greater than 0[/]")
        sys.exit(1)
    if args.repeat < 0:
        Console().print("[red]Error: Repeat must be 0 or greater[/]")
        sys.exit(1)

    ui = RichUI()
    storage = StorageService()

    file_path = Path(args.file)

    if not storage.exists(file_path):
        ui.error(f"File not found: {file_path}")
        sys.exit(1)

    recording = storage.load(file_path)

    ui.header()
    ui.info(f"Playing: [bold]{recording.metadata.name}[/]")
    ui.info(f"Speed: [bold]{args.speed}x[/] | Repeat: [bold]{'inf' if args.repeat == 0 else args.repeat}[/]")
    ui.console.print()

    player = MacroPlayer(recording, speed=args.speed, repeat=args.repeat)
    playback_ui = PlaybackUI(ui.console)
    player.add_observer(playback_ui)

    player.play()
