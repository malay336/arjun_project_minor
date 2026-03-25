import vosk
import sounddevice as sd
import json
import queue
import sys

def listen_for_wake_word(model_path, keyword='jarvis'):
    """
    Listens for the wake word using Vosk.
    This is a 100% offline and free alternative to Picovoice.
    """
    try:
        model = vosk.Model(model_path)
        # Using a restricted grammar for keyword spotting (higher accuracy/speed)
        rec = vosk.KaldiRecognizer(model, 16000, f'["{keyword}", "[unk]"]')
        
        q = queue.Queue()

        def callback(indata, frames, time, status):
            if status:
                print(status, file=sys.stderr)
            q.put(bytes(indata))

        print(f"Listening for wake word '{keyword.upper()}' (Vosk)...")

        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=callback):
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    res = json.loads(rec.Result())
                    if keyword in res.get('text', ''):
                        print(f"Wake word '{keyword}' detected!")
                        return True
                else:
                    partial = json.loads(rec.PartialResult())
                    if keyword in partial.get('partial', ''):
                        print(f"Wake word '{keyword}' detected (partial)!")
                        return True
    except Exception as e:
        print(f"Error in Vosk wake word detection: {e}")
        return False

if __name__ == "__main__":
    # Test path - update to match your local setup
    MODEL_PATH = "models/vosk/vosk-model-small-en-in-0.4"
    listen_for_wake_word(MODEL_PATH)
