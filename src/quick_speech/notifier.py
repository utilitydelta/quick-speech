"""Sound notification module."""

import sys
import threading
import wave
from pathlib import Path

import numpy as np
import sounddevice as sd


class SoundNotifier:
    """Plays notification sounds."""

    def __init__(self, assets_dir: Path | None = None):
        if assets_dir is None:
            assets_dir = Path(__file__).parent.parent.parent / "assets"

        self._start_file = assets_dir / "start.wav"
        self._ding_file = assets_dir / "ding.wav"

        if sys.platform != "win32":
            self._start_data, self._start_rate = self._load_wav(self._start_file)
            self._ding_data, self._ding_rate = self._load_wav(self._ding_file)

    def _load_wav(self, sound_file: Path) -> tuple[np.ndarray | None, int | None]:
        """Load a WAV file and return audio data and sample rate."""
        if not sound_file.exists():
            print(f"Warning: Sound file not found: {sound_file}")
            return None, None

        with wave.open(str(sound_file), "rb") as wf:
            sample_rate = wf.getframerate()
            n_frames = wf.getnframes()
            audio_bytes = wf.readframes(n_frames)
            dtype = np.int16 if wf.getsampwidth() == 2 else np.int8
            audio_data = np.frombuffer(audio_bytes, dtype=dtype)
            audio_data = audio_data.astype(np.float32) / np.iinfo(dtype).max
            return audio_data, sample_rate

    def _play_windows(self, sound_file: Path, wait: bool) -> None:
        """Play sound on Windows using winsound (no console window)."""
        if not sound_file.exists():
            return
        import winsound

        if wait:
            winsound.PlaySound(str(sound_file), winsound.SND_FILENAME)
        else:
            threading.Thread(
                target=winsound.PlaySound,
                args=(str(sound_file), winsound.SND_FILENAME),
                daemon=True,
            ).start()

    def play_start(self, wait: bool = True) -> None:
        """Play a sound indicating recording has started."""
        if sys.platform == "win32":
            self._play_windows(self._start_file, wait)
        elif self._start_data is not None:
            sd.play(self._start_data, self._start_rate)
            if wait:
                sd.wait()

    def play_ding(self, wait: bool = True) -> None:
        """Play the notification sound for completion."""
        if sys.platform == "win32":
            self._play_windows(self._ding_file, wait)
        elif self._ding_data is not None:
            sd.play(self._ding_data, self._ding_rate)
            if wait:
                sd.wait()
