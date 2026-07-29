<div align="center">

# Ripple Voice

English · <a href="README.RU.md">Russian</a>

</div>

Voice dictation for Windows. Press — speak — text inserted. Your voice, in flow.

![Ripple Voice](topic.gif)

## Why

Windows has built-in voice dictation (Win+H), but it:
- Sends your voice to the Microsoft cloud
- Slow and inaccurate
- Doesn't work offline
- Clunky interface

**Ripple Voice** does the same thing, but:
- **Fully offline** — the model runs on your computer
- **Fast** — CUDA GPU accelerates recognition 10x+
- **Private** — your voice never leaves your computer
- **Beautiful** — animated HUD shows what's happening

## How it works

![Animation](animation.gif)

1. **Press the hotkey** — HUD appears, recording starts
2. **Speak** — bars pulse to your voice, the circle shows volume
3. **Release the key** — recording stops, speech is transcribed
4. **Text is inserted** into the active field (Notepad, Word, browser — anywhere)

That's it. No windows, no buttons — just speak and text appears.

## Installation

```powershell
git clone https://github.com/Ap3x0s/Ripple-Voice.git
cd Ripple-Voice
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Running

```powershell
# Via venv (recommended)
Ripple Voice.bat

# Or manually
.venv\Scripts\python.exe main.py
```

On first launch, the model is downloaded automatically (~1.5 GB). After that it works offline.

## GPU (CUDA)

If you have an NVIDIA GPU, the app will automatically use CUDA for faster recognition:

| Device | Speed (medium) | Quality |
|--------|----------------|---------|
| CPU (int8) | ~8-12 sec | Excellent |
| CUDA (float16) | ~0.5-1 sec | Excellent |

Device selection: **Settings → Device → CUDA (GPU) / CPU / Auto**

CUDA requirements:
- NVIDIA GPU with CUDA support (GTX 10xx or newer)
- NVIDIA drivers installed
- PyTorch with CUDA (included in installation)

If you encounter `cublas64_12.dll not found` error, additionally install:
```powershell
pip install nvidia-cublas-cu12
```

## Usage

| Action | Result |
|--------|--------|
| **Hotkey (hold)** | Start recording |
| **Hotkey (release)** | Insert text |
| **Escape** | Cancel recording |
| **Right-click tray icon** | Settings / Exit |

## Settings

Right-click the tray icon → **Settings**. In the settings window you can change:

- Hotkey and recording mode (hold / toggle)
- Speech recognition language
- Device (GPU CUDA / CPU)
- Whisper model (tiny → large-v3)
- HUD theme
- Interface language (English / Русский)
- Punctuation

All changes apply immediately after clicking "Save" — no restart needed. Settings are stored in `~/Documents/ripple-voice/settings.json`.

## HUD Themes

| Theme | Style |
|-------|-------|
| `google` | Soft, minimalistic |
| `google_v2` | Premium with spring physics |
| `hybrid_v2` | ★ Default — bars + timer + volume circle |
| `vercel` | Sharp, cyber-style |

## Whisper Models

| Model | Size | Speed (CPU) | Speed (CUDA) | Quality |
|-------|------|-------------|--------------|---------|
| `tiny` | 75 MB | Fast | Instant | Average |
| `base` | 150 MB | Moderate | Instant | Good |
| `small` | 500 MB | Moderate | Instant | Excellent |
| `medium` | 1.5 GB | Slow | ~1 sec | Excellent |
| `large-v3` | 3 GB | Very slow | ~1-2 sec | Maximum |

Recommendation: `medium` + CUDA — best balance of speed and quality.

## Project Structure

```
Ripple-Voice/
├── main.py              # Entry point, ties everything together
├── audio_recorder.py    # Microphone audio recording
├── transcriber.py       # Speech recognition (faster-whisper)
├── text_inserter.py     # Text insertion into active window
├── hotkey_manager.py    # Global hotkey interception
├── settings.py          # Settings management
├── settings_window.py   # Settings window (PyQt6)
├── stats.py             # Session statistics
├── history.py           # Recognition history
├── hud_window.py        # HUD theme manager
├── hud_hybrid_v2.py     # Default HUD theme
├── hud_google.py        # Google theme
├── hud_google_v2.py     # Google v2 theme
├── hud_vercel.py        # Vercel theme
├── tray_icon.py         # System tray icon
├── requirements.txt     # Python dependencies
├── Ripple Voice.bat     # Quick launcher (Windows)
└── assets/              # Icons and logos
```

## Requirements

- Windows 10/11
- Python 3.10+
- Microphone
- NVIDIA GPU (optional, for CUDA acceleration)

## Privacy

- Speech is processed **locally** on your computer
- No data is sent to the internet
- The model is downloaded once on first launch
- History and settings are stored only on your machine: `~/Documents/ripple-voice/`

## License

MIT
