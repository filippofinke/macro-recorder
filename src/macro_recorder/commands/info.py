import sys
from pathlib import Path

from macro_recorder.storage import StorageService
from macro_recorder.ui import RichUI


def cmd_info(args) -> None:
    ui = RichUI()
    storage = StorageService()

    file_path = Path(args.file)

    if not storage.exists(file_path):
        ui.error(f"File not found: {file_path}")
        sys.exit(1)

    recording = storage.load(file_path)
    ui.header()
    ui.show_recording_stats(recording)
