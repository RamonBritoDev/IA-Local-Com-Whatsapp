from flask import Flask, request, jsonify
import logging
from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG, WAHA_API_URL, WHISPER_MODEL_SIZE
from src.waha_client import send_waha_message
from src.ollama_client import generate_response
from src.audio_processor import download_and_process_audio

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        logging.info("Webhook recebido")

        if isinstance(data, list) and len(data) > 0:
            data = data[0]
            if "body" in data and isinstance(data["body"], dict):
                data = data["body"]

        if "event" in data and data["event"] == "message" and "payload" in data:
            session_name = data.get("session", "default")
            payload = data["payload"]

            if payload.get("fromMe", False):
                return jsonify({'status': 'ignored', 'reason': 'message from me'}), 200

            message_id = payload.get("id", "")
            sender_id = payload.get("from", "")
            has_media = payload.get("hasMedia", False)
            message_type = payload.get("type", "")

            if not sender_id or not message_id:
                return jsonify({'error': 'Mensagem inválida'}), 400

            if has_media and message_type in ["audio", "ptt"]:
                logging.info(f"Recebido {message_type} de {sender_id}")
                send_waha_message(session_name, sender_id, "🔄 Processando seu áudio...")
                transcription, error = download_and_process_audio(session_name, message_id, message_type)

                if error:
                    send_waha_message(session_name, sender_id, f"❌ {error}")
                    return jsonify({'error': error}), 400

                send_waha_message(session_name, sender_id, f"🎤 Transcrição: {transcription}")
                ai_response = generate_response(transcription)
                success, response_data = send_waha_message(session=session_name, to=sender_id, message=ai_response)

                return jsonify({
                    'success': success,
                    'message': 'Áudio processado com sucesso',
                    'transcription': transcription,
                    'response': ai_response,
                    'waha_response': response_data
                })

            elif "body" in payload:
                message_body = payload["body"]
                ai_response = generate_response(message_body)
                success, response_data = send_waha_message(session=session_name, to=sender_id, message=ai_response)

                return jsonify({
                    'success': success,
                    'message': 'Texto processado com sucesso',
                    'response': ai_response,
                    'waha_response': response_data
                })
            else:
                logging.info(f"Mensagem de tipo não suportado: {message_type}")
                return jsonify({'status': 'ignored', 'reason': 'unsupported message type'}), 200
        else:
            return jsonify({'error': 'Formato de webhook não reconhecido'}), 400

    except KeyError as e:
        logging.error(f"Campo obrigatório ausente: {str(e)}")
        return jsonify({'error': f'Campo obrigatório ausente: {str(e)}'}), 400
    except Exception as e:
        logging.error(f"Erro no processamento: {str(e)}")
        return jsonify({'error': f'Erro no processamento: {str(e)}'}), 500

if __name__ == '__main__':
    logging.info(f"Iniciando servidor Flask na porta {FLASK_PORT}")
    logging.info(f"Configurado para usar WAHA em {WAHA_API_URL}")
    logging.info(f"Modelo Whisper: {WHISPER_MODEL_SIZE}")
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
