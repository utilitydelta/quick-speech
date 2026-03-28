"""Main entry point for Quick Speech application."""

import signal
import subprocess
import sys
import threading
import time
from enum import Enum, auto

import pyperclip
from pynput import keyboard

from .notifier import SoundNotifier
from .recorder import AudioRecorder
from .transcriber import Transcriber


def set_system_mute(mute: bool) -> None:
    """Mute or unmute system audio."""
    if sys.platform == "win32":
        _set_system_mute_windows(mute)
    elif sys.platform == "darwin":
        _set_system_mute_macos(mute)
    else:
        _set_system_mute_linux(mute)


def _set_system_mute_macos(mute: bool) -> None:
    """Mute or unmute system audio using osascript on macOS."""
    subprocess.run(
        ["osascript", "-e", f"set volume output muted {'true' if mute else 'false'}"],
        capture_output=True,
    )


def _set_system_mute_linux(mute: bool) -> None:
    """Mute or unmute system audio using PipeWire on Linux."""
    subprocess.run(
        ["wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "1" if mute else "0"],
        capture_output=True,
    )


def _set_system_mute_windows(mute: bool) -> None:
    """Mute or unmute system audio using pycaw on Windows."""
    from pycaw.pycaw import AudioUtilities

    speakers = AudioUtilities.GetSpeakers()
    speakers.EndpointVolume.SetMute(mute, None)


class State(Enum):
    """Application states."""

    IDLE = auto()
    RECORDING = auto()
    TRANSCRIBING = auto()


class QuickSpeech:
    """Main application class."""

    def __init__(self):
        self.state = State.IDLE
        self.recorder = AudioRecorder(sample_rate=16000, channels=1)
        self.transcriber: Transcriber | None = None  # Lazy load
        self.notifier = SoundNotifier()
        self._pressed_keys: set = set()
        self._cmd_keys = {keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r}

    def _ensure_transcriber(self) -> None:
        """Load transcriber on first use."""
        if self.transcriber is None:
            self.transcriber = Transcriber()

    def _on_press(self, key: keyboard.Key | keyboard.KeyCode) -> None:
        """Handle key press events."""
        self._pressed_keys.add(key)
        # Only trigger on F12 press when Super is already held
        if key == keyboard.Key.f12:
            if self._pressed_keys & self._cmd_keys:
                self.toggle_recording()

    def _on_release(self, key: keyboard.Key | keyboard.KeyCode) -> None:
        """Handle key release events."""
        self._pressed_keys.discard(key)

    def toggle_recording(self) -> None:
        """Toggle between recording and idle states."""
        if self.state == State.IDLE:
            self._start_recording()
        elif self.state == State.RECORDING:
            self._stop_and_transcribe()

    def _start_recording(self) -> None:
        """Start recording audio."""
        self.state = State.RECORDING
        self.notifier.play_start(wait=True)
        if sys.platform == "win32":
            time.sleep(0.2)  # Windows needs extra time for audio buffer to flush
        set_system_mute(True)
        self.recorder.start()
        print("Recording... (press Super+F12 to stop)")

    def _stop_and_transcribe(self) -> None:
        """Stop recording and transcribe the audio."""
        self.state = State.TRANSCRIBING
        set_system_mute(False)
        print("Processing...")

        # Stop recording and get audio
        audio = self.recorder.stop()

        if len(audio) == 0:
            print("No audio recorded.")
            self.state = State.IDLE
            return

        # Ensure transcriber is loaded
        self._ensure_transcriber()

        # Transcribe
        text = self.transcriber.transcribe(audio)

        if text:
            # Copy to clipboard
            pyperclip.copy(text)
            print(f"Transcribed: {text}")
            print("(copied to clipboard)")
        else:
            print("No speech detected.")

        # Play notification sound
        self.notifier.play_ding(wait=False)

        self.state = State.IDLE

    def run(self) -> None:
        """Run the application."""
        print("Quick Speech ready.")
        print("Press Super+F12 to start/stop recording.")
        print("Press Ctrl+C to exit.")
        print()

        # Set up keyboard listener
        listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release,
        )
        listener.start()

        # Handle Ctrl+C properly on Windows
        stop_event = threading.Event()

        def handle_exit(signum, frame):
            stop_event.set()

        signal.signal(signal.SIGINT, handle_exit)
        signal.signal(signal.SIGTERM, handle_exit)

        while not stop_event.wait(timeout=1.0):
            pass

        print("\nExiting...")
        listener.stop()


def main() -> None:
    """Entry point."""
    app = QuickSpeech()
    app.run()


if __name__ == "__main__":
    main()
