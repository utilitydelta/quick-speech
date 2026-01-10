# Quick Speech

Speech-to-text application for Ubuntu Linux using OpenAI Whisper with global F12 hotkey.

## Installation

```bash
# 1. Install system dependencies
sudo apt install -y python3-venv python3-dev portaudio19-dev libasound2-dev xclip

# 2. Create virtual environment and install
cd /home/utilitydelta/repos/utilitydelta/quick-speech
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## Usage

```bash
# Start the application
quick-speech

# Or run directly
python -m quick_speech.main
```

**Controls:**
- Press **F12** to start recording
- Press **F12** again to stop, transcribe, and copy to clipboard
- **Ctrl+C** to exit

## Configuration

Change Whisper model via environment variable:

```bash
# Faster, less accurate
QUICK_SPEECH_MODEL=tiny.en quick-speech

# Default (good balance)
QUICK_SPEECH_MODEL=base.en quick-speech

# More accurate, slower
QUICK_SPEECH_MODEL=small.en quick-speech
```

## Notes

- First run downloads the Whisper model (~150MB for base.en)
- Works on X11 sessions (use "GNOME on Xorg" if on Wayland)
- Requires microphone access
