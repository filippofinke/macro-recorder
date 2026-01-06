from pathlib import Path

from macro_recorder.core import MacroRecorder
from macro_recorder.storage import StorageService
from macro_recorder.ui import RichUI, RecordingUI


def cmd_record(args) -> None:
    ui = RichUI()
    storage = StorageService()

    output_path = Path(args.output) / f"{args.name}.json"

    ui.header()
    ui.info(f"Recording: [bold]{args.name}[/]")
    ui.info(f"Output: [dim]{output_path}[/]")
    ui.show_shortcuts()
    ui.console.print()

    ui.countdown(args.delay)

    recorder = MacroRecorder(name=args.name)
    recording_ui = RecordingUI(ui.console)
    recorder.add_observer(recording_ui)

    recorder.start()
    recording = recorder.stop()

    storage.save(recording, output_path)
    ui.console.print()
    ui.show_recording_stats(recording)
