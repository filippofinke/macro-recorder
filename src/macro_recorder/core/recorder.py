import time
import threading
from typing import Optional
from pynput import mouse, keyboard
from pynput.mouse import Button

from macro_recorder.models.mouse_event import MouseEvent
from macro_recorder.models.event_type import EventType
from macro_recorder.models.recording import Recording
from macro_recorder.models.recording_metadata import RecordingMetadata
from macro_recorder.observers.recording_observer import RecordingObserver


class MacroRecorder:
    PAUSE_KEY = keyboard.Key.space

    def __init__(self, name: str):
        self.name = name
        self.events: list[MouseEvent] = []
        self.is_recording = False
        self.is_paused = False
        self.start_time: float = 0
        self.pause_start: float = 0
        self.total_pause_time: float = 0
        self._cmd_pressed = False
        self._mouse_listener: Optional[mouse.Listener] = None
        self._keyboard_listener: Optional[keyboard.Listener] = None
        self._observers: list[RecordingObserver] = []
        self._stop_event = threading.Event()

    def add_observer(self, observer: RecordingObserver) -> None:
        self._observers.append(observer)

    def _notify_event(self, event: MouseEvent) -> None:
        for observer in self._observers:
            observer.on_event(event)

    def _notify_start(self) -> None:
        for observer in self._observers:
            observer.on_start()

    def _notify_stop(self, metadata: RecordingMetadata) -> None:
        for observer in self._observers:
            observer.on_stop(metadata)

    def _notify_pause(self) -> None:
        for observer in self._observers:
            observer.on_pause()

    def _notify_resume(self) -> None:
        for observer in self._observers:
            observer.on_resume()

    def _get_timestamp(self) -> float:
        if self.is_paused:
            return self.pause_start - self.start_time - self.total_pause_time
        return time.time() - self.start_time - self.total_pause_time

    def _on_move(self, x: int, y: int) -> None:
        if self.is_recording and not self.is_paused:
            event = MouseEvent(
                event_type=EventType.MOVE,
                x=x,
                y=y,
                timestamp=self._get_timestamp()
            )
            self.events.append(event)
            self._notify_event(event)

    def _on_click(self, x: int, y: int, button: Button, pressed: bool) -> None:
        if self.is_recording and not self.is_paused:
            event = MouseEvent(
                event_type=EventType.CLICK,
                x=x,
                y=y,
                timestamp=self._get_timestamp(),
                button=button.name,
                pressed=pressed
            )
            self.events.append(event)
            self._notify_event(event)

    def _on_scroll(self, x: int, y: int, dx: int, dy: int) -> None:
        if self.is_recording and not self.is_paused:
            event = MouseEvent(
                event_type=EventType.SCROLL,
                x=x,
                y=y,
                timestamp=self._get_timestamp(),
                dx=dx,
                dy=dy
            )
            self.events.append(event)
            self._notify_event(event)

    def _on_key_press(self, key) -> Optional[bool]:
        if key in (keyboard.Key.cmd, keyboard.Key.cmd_r):
            self._cmd_pressed = True
            return None

        if hasattr(key, 'char') and key.char == 'r' and self._cmd_pressed:
            self.stop()
            return False

        if key == self.PAUSE_KEY and self._cmd_pressed:
            self._toggle_pause()

        return None

    def _on_key_release(self, key) -> None:
        if key in (keyboard.Key.cmd, keyboard.Key.cmd_r):
            self._cmd_pressed = False

    def _toggle_pause(self) -> None:
        if not self.is_recording:
            return

        if self.is_paused:
            self.total_pause_time += time.time() - self.pause_start
            self.is_paused = False
            self._notify_resume()
        else:
            self.pause_start = time.time()
            self.is_paused = True
            self._notify_pause()

    def start(self) -> None:
        self.events = []
        self.start_time = time.time()
        self.total_pause_time = 0
        self.is_recording = True
        self.is_paused = False
        self._stop_event.clear()

        self._notify_start()

        self._mouse_listener = mouse.Listener(
            on_move=self._on_move,
            on_click=self._on_click,
            on_scroll=self._on_scroll
        )
        self._mouse_listener.start()

        self._keyboard_listener = keyboard.Listener(
            on_press=self._on_key_press,
            on_release=self._on_key_release
        )
        self._keyboard_listener.start()
        self._keyboard_listener.join()

        if self._mouse_listener:
            self._mouse_listener.stop()

    def stop(self) -> Recording:
        self.is_recording = False
        self._stop_event.set()

        duration = self._get_timestamp()

        click_count = sum(1 for e in self.events if e.event_type == EventType.CLICK and e.pressed)
        scroll_count = sum(1 for e in self.events if e.event_type == EventType.SCROLL)
        move_count = sum(1 for e in self.events if e.event_type == EventType.MOVE)

        metadata = RecordingMetadata(
            name=self.name,
            duration=duration,
            event_count=len(self.events),
            click_count=click_count,
            scroll_count=scroll_count,
            move_count=move_count
        )

        self._notify_stop(metadata)

        return Recording(metadata=metadata, events=self.events.copy())
