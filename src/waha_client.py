import requests
import logging
from config import WAHA_API_URL, WAHA_API_KEY

def send_waha_message(session, to, message):
    """
    Envia mensagem via WAHA API
    """
    try:
        endpoint = f"{WAHA_API_URL}/api/sendText"
        payload = {
            "session": session,
            "chatId": to,
            "text": message,
            "quotedMsgId": None
        }
        headers = {}
        if WAHA_API_KEY:
            headers["X-Api-Key"] = WAHA_API_KEY

        logging.info(f"Enviando resposta via WAHA para {to}")
        response = requests.post(endpoint, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        response_data = response.json()

        if response_data.get("success", False):
            logging.info(f"Mensagem enviada com sucesso: {response_data.get('id', 'N/A')}")
            return True, response_data
        else:
            logging.error(f"Falha ao enviar mensagem: {response_data.get('error', 'Erro desconhecido')}")
            return False, response_data

    except Exception as e:
        logging.error(f"Erro ao enviar mensagem via WAHA: {str(e)}")
        return False, {"error": str(e)}

def download_media(session, message_id):
    """
    Baixa mídia do WhatsApp usando a API WAHA
    """
    try:
        endpoint = f"{WAHA_API_URL}/api/downloadMedia"
        payload = {
            "session": session,
            "messageId": message_id
        }
        headers = {}
        if WAHA_API_KEY:
            headers["X-Api-Key"] = WAHA_API_KEY

        logging.info(f"Baixando mídia da mensagem: {message_id}")
        response = requests.post(endpoint, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        response_data = response.json()

        if not response_data.get("success", False):
            logging.error(f"Falha ao baixar mídia: {response_data.get('error', 'Erro desconhecido')}")
            return None

        media_base64 = response_data.get("base64")
        if not media_base64:
            logging.error("Base64 da mídia não encontrado na resposta")
            return None

        return media_base64

    except Exception as e:
        logging.error(f"Erro ao baixar mídia: {str(e)}")
        return None
