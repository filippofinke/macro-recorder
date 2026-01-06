from dataclasses import dataclass, asdict, field

from macro_recorder.models.mouse_event import MouseEvent
from macro_recorder.models.recording_metadata import RecordingMetadata


@dataclass
class Recording:
    metadata: RecordingMetadata
    events: list[MouseEvent] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "metadata": asdict(self.metadata),
            "events": [e.to_dict() for e in self.events]
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Recording":
        metadata = RecordingMetadata(**data["metadata"])
        events = [MouseEvent.from_dict(e) for e in data["events"]]
        return cls(metadata=metadata, events=events)
