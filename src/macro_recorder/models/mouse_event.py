from dataclasses import dataclass, asdict
from typing import Optional

from macro_recorder.models.event_type import EventType


@dataclass
class MouseEvent:
    event_type: EventType
    x: int
    y: int
    timestamp: float
    button: Optional[str] = None
    pressed: Optional[bool] = None
    dx: Optional[int] = None
    dy: Optional[int] = None

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}

    @classmethod
    def from_dict(cls, data: dict) -> "MouseEvent":
        if "event_type" in data:
            data["event_type"] = EventType(data["event_type"])
        return cls(**data)
