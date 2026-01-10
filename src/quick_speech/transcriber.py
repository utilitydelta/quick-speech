"""Whisper transcription module using faster-whisper."""

import os

import numpy as np
from faster_whisper import WhisperModel


class Transcriber:
    """Transcribes audio using Whisper."""

    def __init__(self, model_size: str | None = None):
        # Allow model override via environment variable
        model_size = model_size or os.environ.get("QUICK_SPEECH_MODEL", "base.en")

        print(f"Loading Whisper model '{model_size}'...")
        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8",  # Faster on CPU
        )
        print("Model loaded.")

    def transcribe(self, audio: np.ndarray) -> str:
        """Transcribe audio data to text."""
        if len(audio) == 0:
            return ""

        segments, _ = self.model.transcribe(
            audio,
            beam_size=5,
            vad_filter=True,  # Skip silence
            vad_parameters={"min_silence_duration_ms": 500},
        )

        text = " ".join(segment.text for segment in segments).strip()
        return text
