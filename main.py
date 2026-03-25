import datetime
import os
import sys

# Add src to path if needed
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from wake_word import listen_for_wake_word
from stt_engine import STTEngine
from tts_engine import TTSEngine
from llm_engine import LLMEngine

class OfflineAssistant:
    def __init__(self, vosk_model_path, piper_model_path):
        self.stt = STTEngine(vosk_model_path)
        self.tts = TTSEngine(piper_model_path)
        self.llm = LLMEngine(model_name="qwen2.5:0.5b")
        self.vosk_model_path = vosk_model_path

    def search_and_play_music(self, song_name):
        """
        Searches the 'music' folder for a matching song and plays it.
        """
        music_dir = os.path.join(os.path.dirname(__file__), 'music')
        if not os.path.exists(music_dir):
            response = "The music folder doesn't exist yet."
            print(f"Assistant: {response}")
            self.tts.speak(response)
            return

        # Find files matching the song name
        files = [f for f in os.listdir(music_dir) if any(ext in f.lower() for ext in ['.mp3', '.wav', '.m4a'])]
        match = None
        for file in files:
            if song_name.lower() in file.lower():
                match = file
                break
        
        if match:
            response = f"Playing {song_name}."
            print(f"Assistant: {response}")
            self.tts.speak(response)
            # Use os.startfile for Windows to open the file in the default player
            os.startfile(os.path.join(music_dir, match))
        else:
            response = f"I couldn't find a song named {song_name} in the music folder."
            print(f"Assistant: {response}")
            self.tts.speak(response)

    def handle_intent(self, text):
        """
        Process the text command. Supports music playback and LLM chat.
        """
        text_lower = text.lower()
        
        if "stop" in text_lower or "exit" in text_lower or "goodbye" in text_lower:
            response = "Goodbye!"
            print(f"Assistant: {response}")
            self.tts.speak(response)
            sys.exit(0)
        
        elif "play" in text_lower:
            # Extract song name (everything after 'play')
            song_name = text_lower.split("play", 1)[1].strip()
            if song_name:
                self.search_and_play_music(song_name)
            else:
                response = "What song would you like me to play?"
                print(f"Assistant: {response}")
                self.tts.speak(response)
        
        else:
            # Use LLM to generate a dynamic response
            response = self.llm.generate_response(text)
            print(f"Assistant: {response}")
            self.tts.speak(response)

    def run(self):
        print("Assistant started. System is offline.")
        while True:
            # 1. Wait for Wake Word (Now using Vosk)
            if listen_for_wake_word(self.vosk_model_path, keyword='jarvis'):
                # 2. Listen for Command
                command = self.stt.listen()
                
                # 3. Handle Command
                if command:
                    self.handle_intent(command)

if __name__ == "__main__":
    # Configuration - Update paths to match your filesystem
    VOSK_MODEL = "models/vosk/vosk-model-small-en-in-0.4"
    PIPER_MODEL = "models/piper/en_US-lessac-medium.onnx"
    
    assistant = OfflineAssistant(VOSK_MODEL, PIPER_MODEL)
    assistant.run()
