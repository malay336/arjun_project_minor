@echo off
echo Starting Offline AI Assistant Setup...

:: Activate the environment
call .\venv\Scripts\activate.bat

echo Installing dependencies (skipping PyAudio to avoid C++ build errors)...
pip install vosk pvporcupine sounddevice piper-tts ollama --timeout 60

echo.
echo Launching the Assistant...
python main.py
pause
