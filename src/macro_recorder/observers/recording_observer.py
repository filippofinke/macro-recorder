from abc import ABC, abstractmethod

from macro_recorder.models.mouse_event import MouseEvent
from macro_recorder.models.recording_metadata import RecordingMetadata


class RecordingObserver(ABC):
    @abstractmethod
    def on_event(self, event: MouseEvent) -> None:
        pass

    @abstractmethod
    def on_start(self) -> None:
        pass

    @abstractmethod
    def on_stop(self, metadata: RecordingMetadata) -> None:
        pass

    @abstractmethod
    def on_pause(self) -> None:
        pass

    @abstractmethod
    def on_resume(self) -> None:
        pass
