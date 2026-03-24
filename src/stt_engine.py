import vosk
import sys
import os
import json
import sounddevice as sd
import queue

class STTEngine:
    def __init__(self, model_path):
        if not os.path.exists(model_path):
            print(f"Model path {model_path} does not exist. Please download a model from https://alphacephei.com/vosk/models")
            sys.exit(1)
        
        self.model = vosk.Model(model_path)
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
        self.q = queue.Queue()

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    def listen(self):
        """
        Listens to the microphone using sounddevice and returns recognized text.
        """
        print("Listening for command...")
        try:
            with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                                  channels=1, callback=self.callback):
                while True:
                    data = self.q.get()
                    if self.recognizer.AcceptWaveform(data):
                        result = json.loads(self.recognizer.Result())
                        text = result.get("text", "")
                        if text:
                            print(f"Recognized: {text}")
                            return text
                    else:
                        # You could also process partial results here
                        pass
        except Exception as e:
            print(f"STT Recording Error: {e}")
            return ""

if __name__ == "__main__":
    # Correct path to the extracted model
    MODEL_PATH = "models/vosk/vosk-model-small-en-us-0.15"
    stt = STTEngine(MODEL_PATH)
    stt.listen()
