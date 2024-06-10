# WhisperClip

WhisperClip is a voice transcription tool that uses OpenAI Whisper to transcribe speech and copy the text to the clipboard. It supports global hotkeys for easy operation.

## Features
- Transcribe speech to clipboard
- Global hotkey support
- Custom word mappings

## Credits
This project is inspired by [interactive-applications/speech-to-clipboard](https://github.com/interactive-applications/speech-to-clipboard).

### Built With
- [OpenAI Whisper](https://github.com/openai/whisper)
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro)
- [pynput](https://github.com/moses-palmer/pynput)

## Installation

### Using `venv` (recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/WhisperClip.git
   cd WhisperClip

2. Create a virtual environment:
    ```bash
    python3 -m venv venv

3. Activate the virtual environment:
- on windows
    ```bash
    venv\Scripts\activate
- on macOS and Linux
    ```bash
    source venv/bin/activate

4. Install the dependencies:
    ```bash
    pip install -r requirements.txt

## Usage

1. Run the application:
    ```bash
    python WhisperClip.py

2. Instructions

- Select the language (English or Portuguese).
- Choose the model (tiny, base, small, medium, large).
- Click "Start" to begin recording.
- Use the global hotkey cmd+shift+r to start/stop recording.
- The transcription will be copied to the clipboard and displayed in the UI.

## Credits

This project is inspired by [interactive-applications/speech-to-clipboard.](https://github.com/interactive-applications/speech-to-clipboard)

Built With

- OpenAI Whisper
- PyQt5
- pynput
- simpleaudio
- sounddevice
- soundfile
- pyperclip