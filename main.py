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

    def handle_intent(self, text):
        """
        Process the text command. Stops if requested, otherwise uses the LLM to generate an answer.
        """
        text_lower = text.lower()
        
        if "stop" in text_lower or "exit" in text_lower or "goodbye" in text_lower:
            response = "Goodbye!"
            print(f"Assistant: {response}")
            self.tts.speak(response)
            sys.exit(0)
        else:
            # Use Phi-3 LLM to generate a dynamic response
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
