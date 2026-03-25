import datetime
import os
import sys
import time
import msvcrt

# Add src to path if needed
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from wake_word import listen_for_wake_word
from stt_engine import STTEngine
from tts_engine import TTSEngine
from llm_engine import LLMEngine

class OfflineAssistant:
    def __init__(self, vosk_model_path, vosk_small_model_path, piper_model_path):
        self.stt = STTEngine(vosk_model_path)
        self.tts = TTSEngine(piper_model_path)
        self.llm = LLMEngine(model_name="qwen2.5:0.5b")
        self.vosk_small_model_path = vosk_small_model_path

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

        # Find files matching the song name using word-level matching
        audio_extensions = ['.mp3', '.wav', '.m4a']
        files = [f for f in os.listdir(music_dir) if any(f.lower().endswith(ext) for ext in audio_extensions)]
        
        # Score each file by how many query words appear in the filename
        query_words = song_name.lower().split()
        best_match = None
        best_score = 0
        
        for file in files:
            file_lower = file.lower()
            score = sum(1 for word in query_words if word in file_lower)
            if score > best_score:
                best_score = score
                best_match = file
        
        # Require at least half the query words to match
        if best_match and best_score >= max(1, len(query_words) // 2):
            response = f"Playing {song_name}."
            print(f"Assistant: {response}")
            self.tts.speak(response)
            # Use os.startfile for Windows to open the file in the default player
            os.startfile(os.path.join(music_dir, best_match))
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
            # 1. Wait for Wake Word (using small model for fast loading)
            if listen_for_wake_word(self.vosk_small_model_path, keyword='computer'):
                # 2. Listen for Command
                command = self.stt.listen()
                
                # 3. Allow user to edit the command if misrecognized
                if command:
                    print(f"\nRecognized: \"{command}\"")
                    print("Press SPACE within 5s to edit, or wait to confirm...", end="", flush=True)
                    
                    # 5-second countdown with spacebar check
                    edit_requested = False
                    deadline = time.time() + 5
                    while time.time() < deadline:
                        remaining = int(deadline - time.time()) + 1
                        print(f"\r Press SPACE within {remaining}s to edit, or wait to confirm...  ", end="", flush=True)
                        if msvcrt.kbhit():
                            key = msvcrt.getch()
                            if key == b' ':
                                edit_requested = True
                                break
                        time.sleep(0.2)
                    
                    if edit_requested:
                        # Let user edit the existing command (pre-filled)
                        print(f"\rEdit command: {command}", end="")
                        # Clear the line and let user type with the original as reference
                        edited = input(f"\rEdit command (original: \"{command}\"): ").strip()
                        if edited:
                            command = edited
                    else:
                        print(f"\r✓ Confirmed: \"{command}\"                                    ")
                    
                    # 4. Handle Command
                    self.handle_intent(command)

if __name__ == "__main__":
    # Configuration - Update paths to match your filesystem
    VOSK_MODEL = "models/vosk/vosk-model-en-in-0.5"          # Big model for STT (accurate)
    VOSK_SMALL = "models/vosk/vosk-model-small-en-in-0.4"    # Small model for wake word (fast)
    PIPER_MODEL = "models/piper/en_US-lessac-medium.onnx"
    
    assistant = OfflineAssistant(VOSK_MODEL, VOSK_SMALL, PIPER_MODEL)
    assistant.run()
