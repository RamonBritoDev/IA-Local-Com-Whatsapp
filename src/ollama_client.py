import requests
import logging
from config import OLLAMA_API_URL, MODEL_NAME

def generate_response(message):
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": message,
            "stream": False
        }
        logging.info(f"Enviando requisição para Ollama: {message[:50]}...")
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=300)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        logging.error(f"Erro com Ollama: {str(e)}")
        return f"Desculpe, ocorreu um erro: {str(e)}"
