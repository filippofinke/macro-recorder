from dataclasses import dataclass, field
import time


@dataclass
class RecordingMetadata:
    name: str
    created_at: float = field(default_factory=time.time)
    duration: float = 0.0
    event_count: int = 0
    click_count: int = 0
    scroll_count: int = 0
    move_count: int = 0
