import os
import base64
import tempfile
import logging
import whisper
from config import WHISPER_MODEL_SIZE
from src.waha_client import download_media

logging.info(f"Carregando modelo Whisper {WHISPER_MODEL_SIZE}...")
whisper_model = whisper.load_model(WHISPER_MODEL_SIZE)
logging.info("Modelo Whisper carregado com sucesso!")

def download_and_process_audio(session, message_id, message_type):
    """
    Baixa e processa áudio do WhatsApp usando a API WAHA
    Suporta tipos 'audio', 'ptt' (push to talk) e outros formatos de áudio
    """
    try:
        audio_base64 = download_media(session, message_id)
        if not audio_base64:
            return None, "Não foi possível baixar o áudio"

        extension = ".ogg" if message_type == "ptt" else ".mp3"
        audio_bytes = base64.b64decode(audio_base64)

        with tempfile.NamedTemporaryFile(suffix=extension, delete=False) as temp_file:
            temp_path = temp_file.name
            temp_file.write(audio_bytes)

        try:
            logging.info(f"Transcrevendo áudio: {temp_path}")
            transcribe_options = {
                "language": "pt",
                "fp16": False,
                "temperature": 0
            }
            result = whisper_model.transcribe(temp_path, **transcribe_options)
            transcription = result["text"].strip()
            logging.info(f"Transcrição concluída ({len(transcription)} caracteres)")
            return transcription, None
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    except Exception as e:
        logging.error(f"Erro na transcrição: {str(e)}")
        return None, f"Erro na transcrição: {str(e)}"
