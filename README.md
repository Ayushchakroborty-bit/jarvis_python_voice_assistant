# Jarvis - Python Voice Assistant

A Python-based voice assistant that combines speech recognition, text-to-speech, web automation, weather API integration, and a locally running Large Language Model (LLM) through Ollama.

The project can understand voice commands, execute predefined tasks, retrieve real-time weather information, and use a local AI model to answer general questions.

## Features

- Voice command recognition
- Text-to-speech responses using pyttsx3
- AI-powered responses using Ollama and Llama 3.2
- Conversation history management
- Real-time weather information using OpenWeather API
- Google search through voice commands
- YouTube search through voice commands
- WhatsApp Web integration
- Wake-word activation using "Jarvis"
- Continuous command mode after activation
- Voice-controlled shutdown
- Automatic microphone calibration for ambient noise

## Technologies Used

- Python
- SpeechRecognition
- pyttsx3
- Ollama
- Llama 3.2 (3B)
- Requests
- Webbrowser
- OpenWeather API

## System Workflow

```text
User
  |
  v
Microphone
  |
  v
Speech Recognition
  |
  v
Command Processing
  |
  +-------------------+-------------------+
  |                   |                   |
  v                   v                   v
Built-in Commands   Weather API       Ollama LLM
  |                   |                   |
  v                   v                   v
Browser Actions    Weather Data       AI Response
  |                   |                   |
  +-------------------+-------------------+
                      |
                      v
                Text-to-Speech
                      |
                      v
                 User Output

