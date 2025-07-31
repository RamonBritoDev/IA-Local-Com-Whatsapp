import os

# Configurações do Ollama
OLLAMA_API_URL = os.environ.get("OLLAMA_API_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.environ.get("MODEL_NAME", "qwen2.5:3b")

# Configurações do WAHA
WAHA_API_URL = os.environ.get("WAHA_API_URL", "http://192.168.18.8:3000")
WAHA_API_KEY = os.environ.get("WAHA_API_KEY", "your_waha_api_key")

# Configurações do Whisper
WHISPER_MODEL_SIZE = os.environ.get("WHISPER_MODEL_SIZE", "base")

# Configurações do Flask
FLASK_HOST = os.environ.get("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.environ.get("FLASK_PORT", 5001))
FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() in ["true", "1"]
