from abc import ABC, abstractmethod

from macro_recorder.models.recording import Recording


class PlaybackObserver(ABC):
    @abstractmethod
    def on_playback_start(self, recording: Recording, total_iterations: int) -> None:
        pass

    @abstractmethod
    def on_iteration_start(self, iteration: int, total: int) -> None:
        pass

    @abstractmethod
    def on_event_played(self, index: int, total: int) -> None:
        pass

    @abstractmethod
    def on_playback_complete(self) -> None:
        pass

    @abstractmethod
    def on_playback_pause(self) -> None:
        pass

    @abstractmethod
    def on_playback_resume(self) -> None:
        pass
