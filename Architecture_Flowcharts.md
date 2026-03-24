# Offline AI Assistant Architecture

This document contains detailed flowcharts explaining the architecture and execution flow of the Offline AI Assistant.

## 1. High-Level System Architecture

This flowchart shows the main components of the system and how they interact with each other.

```mermaid
graph TD
    User((User))
    
    subgraph Offline Assistant [Offline AI Assistant]
        Main[Main Controller\nmain.py]
        WakeWord[Wake Word Engine\nsrc/wake_word.py]
        STT[Speech-to-Text Engine\nsrc/stt_engine.py]
        LLM[LLM Engine\nsrc/llm_engine.py]
        TTS[Text-to-Speech Engine\nsrc/tts_engine.py]
    end

    subgraph External Dependencies
        Porcupine[Picovoice Porcupine\nWake Word]
        Vosk[Vosk Model\nSTT]
        Ollama[Ollama / Phi-3\nLLM]
        Piper[Piper TTS Model\nTTS]
    end

    %% User Interactions
    User -- "Speaks 'Jarvis'" --> WakeWord
    User -- "Speaks Command" --> STT
    TTS -- "Plays Audio" --> User

    %% Internal Component Interactions
    Main -- "1. Start Listening" --> WakeWord
    WakeWord -- "2. Wake Word Detected" --> Main
    Main -- "3. Start Recording" --> STT
    STT -- "4. Returns Transcribed Text" --> Main
    Main -- "5. Send Prompt" --> LLM
    LLM -- "6. Returns Text Response" --> Main
    Main -- "7. Send Text to Speak" --> TTS
    
    %% Dependency Connections
    WakeWord -.-> Porcupine
    STT -.-> Vosk
    LLM -.-> Ollama
    TTS -.-> Piper
```

---

## 2. Detailed Execution Flow

This sequence diagram illustrates the step-by-step execution flow from the moment the program starts to when an interaction finishes.

```mermaid
sequenceDiagram
    participant User
    participant Main as Main (main.py)
    participant WW as WakeWord (Porcupine)
    participant STT as STT (Vosk)
    participant LLM as LLM (Ollama/Phi-3)
    participant TTS as TTS (Piper)
    
    Main->>Main: Initialize Components (Vosk, Piper, Ollama)
    Main->>WW: listen_for_wake_word(sensitivity=0.4)
    Note over WW: Listening for "Jarvis"...
    
    User->>WW: "Jarvis"
    WW-->>Main: True (Wake Word Detected)
    
    Main->>STT: listen()
    Note over STT: Recording via sounddevice...
    User->>STT: "What is the capital of India?"
    STT-->>Main: Recognized Text: "what is the capital of india"
    
    Main->>Main: handle_intent("what is the capital of india")
    
    alt Command is "stop", "exit", or "goodbye"
        Main->>TTS: speak("Goodbye!")
        TTS-->>User: Plays "Goodbye!" audio
        Main->>Main: sys.exit(0)
    else Other commands
        Main->>LLM: generate_response(text)
        Note over LLM: Sending prompt to local Phi-3...
        LLM-->>Main: Text Response
        Main->>TTS: speak(response)
        Note over TTS: Generating & Playing Audio...
        TTS-->>User: Plays generated speech audio
    end
    
    Main->>WW: loop back: listen_for_wake_word()
```

---

## 3. Data Flow Diagram

This diagram shows how data transforms as it moves through the system.

```mermaid
flowchart LR
    AudioIn[Microphone Audio\nFloat32 / Int16 PCM]
    
    subgraph Processing Pipeline
        WW[Wake Word\nPattern Matching]
        STT[Vosk STT\nKaldi Recognizer]
        LLM[Ollama\nPhi-3 Inference]
        TTS[Piper\nONNX Inference]
    end
    
    AudioOut[Speaker Audio\nWAV File / Playback]

    AudioIn -- Stream --> WW
    AudioIn -- Stream --> STT
    
    WW -- Boolean Trigger --> STT
    STT -- JSON -> String --> LLM
    LLM -- String --> TTS
    TTS -- File Path -> CMD Execution --> AudioOut
```
