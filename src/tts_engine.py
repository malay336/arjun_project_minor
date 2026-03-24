import subprocess
import os

class TTSEngine:
    def __init__(self, model_path, piper_path="piper"):
        """
        Initializes the TTS engine.
        model_path: Path to the .onnx model file.
        piper_path: Path to the piper executable (if not in PATH).
        """
        self.model_path = model_path
        self.piper_path = piper_path
        
        if not os.path.exists(model_path):
            print(f"Model file {model_path} not found.")
            # We don't exit here to allow manual setup
        
    def speak(self, text, output_file="output.wav"):
        """
        Converts text to speech using Piper and plays it.
        """
        if not text:
            return

        try:
            # Command to generate speech
            # Example: echo "text" | piper --model model.onnx --output_file output.wav
            process = subprocess.Popen(
                [self.piper_path, "--model", self.model_path, "--output_file", output_file],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(input=text)

            if process.returncode == 0:
                print(f"Generated speech: {output_file}")
                self.play_audio(output_file)
            else:
                print(f"Piper error: {stderr}")

        except Exception as e:
            print(f"TTS Error: {e}")

    def play_audio(self, file_path):
        """
        Plays the generated audio file.
        On Windows, we can use 'start' or a python library.
        """
        if os.name == 'nt':
            os.system(f"start /min powershell -c (New-Object Media.SoundPlayer '{file_path}').PlaySync()")
        else:
            # On Linux, use aplay or similar
            os.system(f"aplay {file_path}")

if __name__ == "__main__":
    # Example usage
    MODEL_PATH = "models/piper/en_US-lessac-medium.onnx"
    tts = TTSEngine(MODEL_PATH)
    tts.speak("Hello, this is your offline assistant.")
