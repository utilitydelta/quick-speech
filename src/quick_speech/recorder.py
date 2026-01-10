"""Audio recording module using sounddevice."""

import numpy as np
import sounddevice as sd


class AudioRecorder:
    """Records audio from the default microphone."""

    def __init__(self, sample_rate: int = 16000, channels: int = 1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = False
        self.frames: list[np.ndarray] = []
        self.stream: sd.InputStream | None = None

    def _callback(self, indata: np.ndarray, frames: int, time_info, status) -> None:
        """Callback for audio stream - stores frames while recording."""
        if status:
            print(f"Audio status: {status}")
        if self.recording:
            self.frames.append(indata.copy())

    def start(self) -> None:
        """Start recording audio."""
        self.recording = True
        self.frames = []
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=np.float32,
            callback=self._callback,
        )
        self.stream.start()

    def stop(self) -> np.ndarray:
        """Stop recording and return the audio data as a numpy array."""
        self.recording = False
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        if not self.frames:
            return np.array([], dtype=np.float32)

        return np.concatenate(self.frames, axis=0).flatten()
