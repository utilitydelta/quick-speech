# Quick Speech

Quick Speech runs in the background while you work. Hit F9 anytime you like, talk into your mic, hit F9 again to stop, and it'll be converted to text and copied into your clipboard. Save all that typing!

- No auto-stop detection, explicit F9 to start, F9 to stop
- Mutes your audio, so you can keep listening to your music :)
- Audio queues for start and stop, so you know its working

This is only tested on Ubuntu Linux x64. Probably doesn't work on anything else. Submit some PRs if you wanna fix that!

## Installation

```bash
# 1. Install system dependencies
sudo apt install -y python3-venv python3-dev portaudio19-dev libasound2-dev xclip

# 2. Create virtual environment and install
cd ~/
git clone https://github.com/utilitydelta/quick-speech
cd ~/quick-speech
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
- Press **F9** to start recording
- Press **F9** again to stop, transcribe, and copy to clipboard
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
