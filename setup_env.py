import os
import sys
import subprocess

def setup_env():
    print("--- Offline AI Assistant Environment Setup ---")
    
    # 1. Create Virtual Environment
    if not os.path.exists("venv"):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    else:
        print("Virtual environment already exists.")

    # 2. Determine pip command
    pip_cmd = os.path.join("venv", "Scripts", "pip") if os.name == "nt" else os.path.join("venv", "bin", "pip")

    # 3. Install Dependencies
    dependencies = [
        "vosk",
        "pvporcupine",
        "sounddevice",
        "piper-tts",
        "pathvalidate",
        "ollama"
    ]
    
    print(f"Installing dependencies: {', '.join(dependencies)}...")
    subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True)
    subprocess.run([pip_cmd, "install"] + dependencies, check=True)

    print("\n--- Setup Complete ---")
    print("To activate the environment:")
    if os.name == "nt":
        print("    .\\venv\\Scripts\\activate")
    else:
        print("    source venv/bin/activate")

if __name__ == "__main__":
    setup_env()
