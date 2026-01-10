"""Main entry point for Quick Speech application."""

import subprocess
import time
from enum import Enum, auto

import pyperclip
from pynput import keyboard

from .notifier import SoundNotifier
from .recorder import AudioRecorder
from .transcriber import Transcriber


def set_system_mute(mute: bool) -> None:
    """Mute or unmute system audio using PipeWire."""
    subprocess.run(
        ["wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "1" if mute else "0"],
        capture_output=True,
    )


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

    def _ensure_transcriber(self) -> None:
        """Load transcriber on first use."""
        if self.transcriber is None:
            self.transcriber = Transcriber()

    def toggle_recording(self) -> None:
        """Toggle between recording and idle states."""
        if self.state == State.IDLE:
            self._start_recording()
        elif self.state == State.RECORDING:
            self._stop_and_transcribe()

    def _start_recording(self) -> None:
        """Start recording audio."""
        self.state = State.RECORDING
        set_system_mute(True)
        self.recorder.start()
        print("Recording... (press F9 to stop)")

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
        print("Press F9 to start/stop recording.")
        print("Press Ctrl+C to exit.")
        print()

        # Set up global hotkey
        hotkeys = keyboard.GlobalHotKeys({"<f9>": self.toggle_recording})
        hotkeys.start()

        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nExiting...")
            hotkeys.stop()


def main() -> None:
    """Entry point."""
    app = QuickSpeech()
    app.run()


if __name__ == "__main__":
    main()
