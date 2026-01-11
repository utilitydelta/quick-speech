# Quick Speech

Quick Speech runs in the background while you work. Hit Super+F12 anytime you like, talk into your mic, hit Super+F12 again to stop, and it'll be converted to text and copied into your clipboard. Save all that typing!

- No auto-stop detection, explicit Super+F12 to start, Super+F12 to stop
- Mutes your audio, so you can keep listening to your music :)
- Audio queues for start and stop, so you know its working

Works on Ubuntu Linux x64 and Windows.

## Installation (Linux)

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

## Installation (Windows)

**Requirements:** Python 3.13 (ML dependencies don't have builds for Python 3.14 yet)

```powershell
# 1. Clone the repository
git clone https://github.com/utilitydelta/quick-speech
cd quick-speech

# 2. Create virtual environment and install
# If you have multiple Python versions, use the py launcher to select 3.13:
py -3.13 -m venv venv
.\venv\Scripts\activate
pip install -e .
```

**Notes:**
- Uses **Win+F12** as the hotkey (Super key maps to Win on Windows)
- Clipboard integration uses the Windows clipboard automatically
- No additional system dependencies required

## Usage

```bash
# Start the application
quick-speech

# Or run directly
python -m quick_speech.main
```

**Controls:**
- Press **Super+F12** to start recording
- Press **Super+F12** again to stop, transcribe, and copy to clipboard
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

## Run at Startup (Linux)

To have Quick Speech start automatically when you log in, create a systemd user service:

```bash
# 1. Create the service file (run from the quick-speech directory)
mkdir -p ~/.config/systemd/user

cat > ~/.config/systemd/user/quick-speech.service << EOF
[Unit]
Description=Quick Speech - Voice to Text
After=graphical-session.target

[Service]
Type=simple
ExecStart=$(pwd)/venv/bin/quick-speech
Restart=on-failure
RestartSec=5
Environment=DISPLAY=$DISPLAY
Environment=XAUTHORITY=$XAUTHORITY

[Install]
WantedBy=default.target
EOF

# 2. Enable and start the service
systemctl --user daemon-reload
systemctl --user enable quick-speech.service
systemctl --user start quick-speech.service
```

**Useful commands:**
- Check status: `systemctl --user status quick-speech.service`
- View logs: `journalctl --user -u quick-speech.service -f`
- Stop: `systemctl --user stop quick-speech.service`
- Disable autostart: `systemctl --user disable quick-speech.service`

## Run at Startup (Windows)

Run this in PowerShell from the quick-speech directory to create a startup shortcut:

```powershell
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\Quick Speech.lnk")
$Shortcut.TargetPath = "$PWD\venv\Scripts\pythonw.exe"
$Shortcut.Arguments = "-m quick_speech.main"
$Shortcut.WorkingDirectory = "$PWD"
$Shortcut.Save()
```

**Useful commands:**
- Remove from startup: `Remove-Item "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\Quick Speech.lnk"`

## Notes

- First run downloads the Whisper model (~150MB for base.en)
- Requires microphone access
- **Linux:** Works on X11 sessions
- **Windows:** Run from a terminal with admin privileges if hotkey registration fails
