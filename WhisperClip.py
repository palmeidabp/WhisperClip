import sys
import time
import re
import simpleaudio as sa
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QRadioButton, QButtonGroup, QLabel, QComboBox, QCheckBox, QTextEdit
import whisper
import sounddevice as sd
import soundfile as sf
import numpy as np
import pyperclip
import threading
import os
from pynput import keyboard
from PyQt5.QtCore import pyqtSignal, QObject  # Ensure QObject is imported

class App(QWidget):
    # Add a signal to update the transcription text
    update_transcription_signal = pyqtSignal(str)
    start_stop_signal = pyqtSignal()  # Add a signal for start/stop

    def __init__(self):
        super().__init__()
        self.models_info = {
            "tiny": "1GB",
            "base": "1GB",
            "small": "2GB",
            "medium": "5GB",
            "large": "10GB"
        }
        self.selected_model = None
        self.recording = False
        self.audio_data = []
        self.word_mappings = self.load_word_mappings("word_mappings.txt")
        self.sound_enabled = True  # Default sound setting
        self.initUI()
        self.setup_hotkeys()  # Setup hotkeys
        self.update_transcription_signal.connect(self.update_transcription)  # Connect the signal to the slot
        self.start_stop_signal.connect(self.on_start_stop)  # Connect the signal to the slot

    def load_word_mappings(self, filepath):
        mappings = {}
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    key, value = line.strip().split(':')
                    mappings[key] = value
        except FileNotFoundError:
            print(f"Warning: Mapping file '{filepath}' not found.")
        return mappings

    def apply_word_mappings(self, text):
        def replace(match):
            word = match.group(0)
            return self.word_mappings.get(word, word)

        pattern = re.compile(r'\b(' + '|'.join(re.escape(key) for key in self.word_mappings.keys()) + r')\b')
        return pattern.sub(replace, text)

    def initUI(self):
        self.layout = QVBoxLayout()

        self.label = QLabel("Select Language:", self)
        self.layout.addWidget(self.label)

        self.lang_group = QButtonGroup(self)
        self.lang_en = QRadioButton("English", self)
        self.lang_en.setChecked(True)
        self.lang_pt = QRadioButton("Portuguese", self)
        self.lang_group.addButton(self.lang_en)
        self.lang_group.addButton(self.lang_pt)
        self.layout.addWidget(self.lang_en)
        self.layout.addWidget(self.lang_pt)

        self.model_label = QLabel("Select Model (VRAM Requirement):", self)
        self.layout.addWidget(self.model_label)

        self.model_combo = QComboBox(self)
        for model_name, vram in self.models_info.items():
            self.model_combo.addItem(f"{model_name} ({vram})")
        self.model_combo.currentIndexChanged.connect(self.on_model_change)
        self.layout.addWidget(self.model_combo)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.on_start_stop)
        self.start_button.setEnabled(False)  # Initially disabled
        self.layout.addWidget(self.start_button)

        self.play_button = QPushButton("Play Recording", self)
        self.play_button.clicked.connect(self.play_recording)
        self.play_button.setEnabled(False)  # Initially disabled
        self.layout.addWidget(self.play_button)

        self.exit_button = QPushButton("Exit", self)
        self.exit_button.clicked.connect(self.close_application)
        self.layout.addWidget(self.exit_button)

        self.info_label = QLabel("", self)
        self.layout.addWidget(self.info_label)

        self.transcription_label = QTextEdit(self)  # {{ edit_1 }}
        self.transcription_label.setReadOnly(True)  # {{ edit_2 }}
        self.layout.addWidget(self.transcription_label)

        self.sound_checkbox = QCheckBox("Enable Sound Notifications", self)
        self.sound_checkbox.setChecked(True)
        self.sound_checkbox.stateChanged.connect(self.toggle_sound)
        self.layout.addWidget(self.sound_checkbox)

        self.setLayout(self.layout)
        self.setWindowTitle('Voice Transcription')
        self.show()

    def setup_hotkeys(self):
        def on_activate():
            self.start_stop_signal.emit()  # Emit the signal instead of calling the method directly

        self.listener = keyboard.GlobalHotKeys({
            '<cmd>+<shift>+r': on_activate
        })
        self.listener.start()

    def record_audio(self, fs=16000):
        self.audio_data = []
        self.recording = True
        with sd.InputStream(samplerate=fs, channels=1, callback=self.audio_callback):
            while self.recording:
                sd.sleep(100)

    def audio_callback(self, indata, frames, time, status):
        if self.recording:
            self.audio_data.append(indata.copy())
        else:
            raise sd.CallbackStop

    def stop_recording(self):
        self.recording = False

    def transcribe_audio(self):
        if not self.audio_data:
            self.info_label.setText("No audio data to transcribe.")
            return 0
        lang = "en" if self.lang_en.isChecked() else "pt"
        audio = np.concatenate(self.audio_data, axis=0).flatten()
        start_time = time.time()
        result = self.selected_model.transcribe(audio, language=lang)
        end_time = time.time()
        transcribe_time = (end_time - start_time) * 1000  # in milliseconds
        transcribed_text = self.apply_word_mappings(result['text'])
        pyperclip.copy(transcribed_text)
        self.info_label.setText(f"Transcription copied to clipboard! Transcription time: {transcribe_time:.2f} ms")
        
        # Emit the signal to update the transcription text
        self.update_transcription_signal.emit(transcribed_text)  # {{ edit_1 }}
        
        print("Transcription copied to clipboard!")
        if self.sound_enabled:
            self.play_notification_sound()
        return transcribe_time

    def start_recording(self):
        self.clear_ui()
        self.record_audio_thread = threading.Thread(target=self.record_audio)
        self.record_audio_thread.start()
        self.start_button.setEnabled(True)  # Enable button so it can be clicked to stop
        self.start_button.setText('Stop')
        self.record_start_time = time.time()

    def on_start_stop(self):
        if self.start_button.text() == 'Start':
            self.start_recording()
        elif self.start_button.text() == 'Stop':
            self.stop_recording()
            self.record_audio_thread.join()
            self.start_button.setText('Processing...')
            self.start_button.setEnabled(False)
            record_time = (time.time() - self.record_start_time) * 1000  # in milliseconds
            transcribe_time = self.transcribe_audio()
            self.start_button.setEnabled(True)
            self.start_button.setText("Start")
            self.play_button.setEnabled(True)  # Enable play button after recording
            if transcribe_time > 0:
                self.info_label.setText(f"Recording length: {record_time:.2f} ms\nTranscription copied to clipboard! Transcription time: {transcribe_time:.2f} ms")
        else:
            print("Unexpected state for start button")

    def clear_ui(self):
        self.info_label.setText("")
        self.transcription_label.setText("")
        self.play_button.setEnabled(False)

    def close_application(self):
        self.recording = False  # Ensure recording stops if running
        self.listener.stop()  # Stop the hotkey listener
        self.close()

    def on_model_change(self, index):
        model_name = list(self.models_info.keys())[index]
        self.load_model(model_name)

    def load_model(self, model_name):
        self.start_button.setEnabled(False)  # Disable start button while loading
        def load():
            self.selected_model = whisper.load_model(model_name)
            self.start_button.setEnabled(True)  # Enable start button after loading
        threading.Thread(target=load).start()

    def play_recording(self):
        if self.audio_data:
            audio_array = np.concatenate(self.audio_data, axis=0)
            sf.write('temp_recording.wav', audio_array, 16000)
            data, fs = sf.read('temp_recording.wav')
            sd.play(data, fs)
            sd.wait()

    def play_notification_sound(self):
        os.system('afplay /System/Library/Sounds/Ping.aiff')

    def toggle_sound(self, state):
        self.sound_enabled = state == 2

    # Add a new method to update the transcription text
    def update_transcription(self, text):
        self.transcription_label.setText(f"Transcription:\n{text}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
