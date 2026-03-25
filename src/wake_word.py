import vosk
import sounddevice as sd
import numpy as np
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
        # Use full vocabulary recognition (no grammar restriction)
        # Grammar mode fails for names like "jarvis" that aren't in the restricted dict
        rec = vosk.KaldiRecognizer(model, 16000)
        rec.SetWords(True)
        
        q = queue.Queue()

        def callback(indata, frames, time, status):
            if status:
                print(status, file=sys.stderr)
            q.put(bytes(indata))

        device_info = sd.query_devices(None, 'input')
        print(f"Using input device: {device_info['name']}")
        print(f"Listening for wake word '{keyword.upper()}'...")

        with sd.RawInputStream(samplerate=16000, blocksize=4000, dtype='int16',
                               channels=1, callback=callback):
            while True:
                data = q.get()
                
                if rec.AcceptWaveform(data):
                    res = json.loads(rec.Result())
                    text = res.get('text', '')
                    if text:
                        print(f"[Heard]: {text}")
                    if keyword in text:
                        print(f"\n>>> Wake word '{keyword}' detected!")
                        return True
                else:
                    partial = json.loads(rec.PartialResult())
                    partial_text = partial.get('partial', '')
                    if keyword in partial_text:
                        print(f"\n>>> Wake word '{keyword}' detected!")
                        return True
    except Exception as e:
        print(f"Error in Vosk wake word detection: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Test path - update to match your local setup
    MODEL_PATH = "models/vosk/vosk-model-small-en-in-0.4"
    listen_for_wake_word(MODEL_PATH)
