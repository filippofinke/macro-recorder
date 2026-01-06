import json
from pathlib import Path

from macro_recorder.models.recording import Recording


class StorageService:
    def save(self, recording: Recording, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(recording.to_dict(), f, indent=2)

    def load(self, path: Path) -> Recording:
        with open(path, "r") as f:
            data = json.load(f)
        return Recording.from_dict(data)

    def exists(self, path: Path) -> bool:
        return path.exists()
