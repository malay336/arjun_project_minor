import pvporcupine
import sounddevice as sd
import numpy as np

def listen_for_wake_word(access_key, sensitivity=0.5):
    """
    Listens for the wake word using Porcupine and sounddevice.
    Sensitivity: 0 to 1. Higher is more sensitive. Default is 0.5.
    """
    porcupine = None

    try:
        # Initialize Porcupine
        porcupine = pvporcupine.create(access_key=access_key, keywords=['jarvis'], sensitivities=[sensitivity])
        
        print("Listening for wake word 'JARVIS'...")

        # Audio callback for sounddevice
        detected = [False]
        def audio_callback(indata, frames, time, status):
            if status:
                print(status)
            # Porcupine handles 16kHz mono audio as int16
            pcm = (indata * 32767).astype(np.int16).flatten()
            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                detected[0] = True
                raise sd.CallbackStop

        # Open InputStream
        with sd.InputStream(
            samplerate=porcupine.sample_rate,
            blocksize=porcupine.frame_length,
            channels=1,
            dtype='float32',
            callback=audio_callback):
            
            # Keep the main thread alive until the callback stops
            while not detected[0]:
                sd.sleep(100)
                
        return True

    except sd.CallbackStop:
        return True
    except Exception as e:
        print(f"Error in wake word detection: {e}")
        return False
    finally:
        if porcupine is not None:
            porcupine.delete()

if __name__ == "__main__":
    # AccessKey is required for Porcupine (get a free one from Picovoice Console)
    ACCESS_KEY = "YOUR_PORCUPINE_ACCESS_KEY" 
    listen_for_wake_word(ACCESS_KEY)
