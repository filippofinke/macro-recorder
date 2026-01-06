import time
import threading
from typing import Optional
from pynput import keyboard
from pynput.mouse import Button, Controller as MouseController

from macro_recorder.models.recording import Recording
from macro_recorder.models.event_type import EventType
from macro_recorder.observers.playback_observer import PlaybackObserver


class MacroPlayer:
    PAUSE_KEY = keyboard.Key.space

    def __init__(self, recording: Recording, speed: float = 1.0, repeat: int = 1):
        self.recording = recording
        self.speed = speed
        self.repeat = repeat
        self.is_playing = False
        self.is_paused = False
        self._cmd_pressed = False
        self._mouse = MouseController()
        self._keyboard_listener: Optional[keyboard.Listener] = None
        self._observers: list[PlaybackObserver] = []
        self._stop_event = threading.Event()

    def add_observer(self, observer: PlaybackObserver) -> None:
        self._observers.append(observer)

    def _notify_start(self) -> None:
        for observer in self._observers:
            observer.on_playback_start(self.recording, self.repeat)

    def _notify_iteration(self, iteration: int, total: int) -> None:
        for observer in self._observers:
            observer.on_iteration_start(iteration, total)

    def _notify_event(self, index: int, total: int) -> None:
        for observer in self._observers:
            observer.on_event_played(index, total)

    def _notify_complete(self) -> None:
        for observer in self._observers:
            observer.on_playback_complete()

    def _notify_pause(self) -> None:
        for observer in self._observers:
            observer.on_playback_pause()

    def _notify_resume(self) -> None:
        for observer in self._observers:
            observer.on_playback_resume()

    def _on_key_press(self, key) -> Optional[bool]:
        if key in (keyboard.Key.cmd, keyboard.Key.cmd_r):
            self._cmd_pressed = True
            return None

        if key == keyboard.Key.esc:
            self.stop()
            return False

        if key == self.PAUSE_KEY and self._cmd_pressed:
            self._toggle_pause()

        return None

    def _on_key_release(self, key) -> None:
        if key in (keyboard.Key.cmd, keyboard.Key.cmd_r):
            self._cmd_pressed = False

    def _toggle_pause(self) -> None:
        if not self.is_playing:
            return

        if self.is_paused:
            self.is_paused = False
            self._notify_resume()
        else:
            self.is_paused = True
            self._notify_pause()

    def _play_events(self) -> None:
        events = self.recording.events
        total_events = len(events)
        iteration = 0
        infinite = self.repeat == 0

        self._notify_start()

        while (infinite or iteration < self.repeat) and not self._stop_event.is_set():
            iteration += 1
            self._notify_iteration(iteration, self.repeat)

            last_timestamp = 0

            for i, event in enumerate(events):
                if self._stop_event.is_set():
                    break

                while self.is_paused and not self._stop_event.is_set():
                    time.sleep(0.05)

                delay = (event.timestamp - last_timestamp) / self.speed
                if delay > 0:
                    time.sleep(delay)
                last_timestamp = event.timestamp

                if event.event_type == EventType.MOVE:
                    self._mouse.position = (event.x, event.y)
                elif event.event_type == EventType.CLICK:
                    button = getattr(Button, event.button)
                    self._mouse.position = (event.x, event.y)
                    if event.pressed:
                        self._mouse.press(button)
                    else:
                        self._mouse.release(button)
                elif event.event_type == EventType.SCROLL:
                    self._mouse.position = (event.x, event.y)
                    self._mouse.scroll(event.dx or 0, event.dy or 0)

                self._notify_event(i + 1, total_events)

        self.is_playing = False
        self._notify_complete()

    def play(self) -> None:
        self.is_playing = True
        self.is_paused = False
        self._stop_event.clear()

        play_thread = threading.Thread(target=self._play_events, daemon=True)
        play_thread.start()

        self._keyboard_listener = keyboard.Listener(
            on_press=self._on_key_press,
            on_release=self._on_key_release
        )
        self._keyboard_listener.start()
        self._keyboard_listener.join()

    def stop(self) -> None:
        self._stop_event.set()
        self.is_playing = False
