"""Sound notification module."""

import wave
from pathlib import Path

import numpy as np
import sounddevice as sd


class SoundNotifier:
    """Plays notification sounds."""

    def __init__(self, sound_file: Path | None = None):
        if sound_file is None:
            # Default to ding.wav in assets directory
            sound_file = Path(__file__).parent.parent.parent / "assets" / "ding.wav"

        if not sound_file.exists():
            print(f"Warning: Sound file not found: {sound_file}")
            self.audio_data = None
            self.sample_rate = None
        else:
            # Load WAV file
            with wave.open(str(sound_file), "rb") as wf:
                self.sample_rate = wf.getframerate()
                n_frames = wf.getnframes()
                audio_bytes = wf.readframes(n_frames)
                # Convert to numpy array
                dtype = np.int16 if wf.getsampwidth() == 2 else np.int8
                self.audio_data = np.frombuffer(audio_bytes, dtype=dtype)
                # Normalize to float32
                self.audio_data = self.audio_data.astype(np.float32) / np.iinfo(dtype).max

    def play_ding(self, wait: bool = True) -> None:
        """Play the notification sound.

        Args:
            wait: If True, block until sound finishes playing.
        """
        if self.audio_data is not None:
            sd.play(self.audio_data, self.sample_rate)
            if wait:
                sd.wait()
