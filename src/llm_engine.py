import ollama

class LLMEngine:
    def __init__(self, model_name="qwen2.5:0.5b"):
        self.model_name = model_name
        # The system prompt sets the personality and restrictions of the assistant
        self.system_prompt = (
            "You are a helpful and concise AI assistant running offline. "
            "Keep your answers short, usually under 2-3 sentences, so they can be spoken aloud quickly. "
            "Do not use markdown formatting like asterisks or code blocks."
        )
        
        # Ensure the lightweight model is pulled on startup
        print(f"[LLM Setup] Checking and pulling model '{self.model_name}'... (This takes a minute on first run)")
        try:
            ollama.pull(self.model_name)
            print(f"[LLM Setup] Model '{self.model_name}' is loaded and ready.")
        except Exception as e:
            print(f"[LLM Setup Warning] Could not connect to Ollama or pull model: {e}")

    def generate_response(self, user_prompt):
        """
        Sends the user's spoken prompt to the local Phi-3 model and returns the text response.
        """
        try:
            print(f"[LLM] Thinking...")
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response['message']['content'].strip()
        except Exception as e:
            error_msg = str(e)
            print(f"[LLM Error] {error_msg}")
            
            # If the GPU runs out of memory, retry the request using only the CPU
            if "out of memory" in error_msg.lower() or "500" in error_msg:
                print(f"[LLM System] GPU memory full. Attempting to fall back to CPU inference for '{self.model_name}'...")
                try:
                    response_cpu = ollama.chat(
                        model=self.model_name,
                        messages=[
                            {"role": "system", "content": self.system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        options={"num_gpu": 0}
                    )
                    return response_cpu['message']['content'].strip()
                except Exception as cpu_error:
                    print(f"[LLM CPU Fallback Error] {cpu_error}")
            
            return "I'm having trouble connecting to my brain. My memory might be full, or Ollama isn't running."
