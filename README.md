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

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

1. **Fork the Project**
2. **Create your Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your Changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the Branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**


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