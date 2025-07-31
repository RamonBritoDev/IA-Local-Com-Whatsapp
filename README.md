# IA Local com WhatsApp

Este projeto integra um assistente de IA local (usando Ollama) com o WhatsApp, permitindo que você converse com a IA e transcreva áudios diretamente do seu celular.

## Funcionalidades

- **Conversa por Texto:** Envie mensagens de texto para a IA e receba respostas geradas localmente.
- **Transcrição de Áudio:** Envie mensagens de áudio (incluindo notas de voz) e receba a transcrição em texto.
- **Integração com WhatsApp:** Usa a API do WAHA (WhatsApp HTTP API) para se conectar à sua conta do WhatsApp.

## Estrutura do Projeto

O projeto foi estruturado de forma modular para facilitar a manutenção e o desenvolvimento:

- `app.py`: O servidor web principal (Flask) que recebe os webhooks do WAHA.
- `config.py`: Centraliza todas as configurações do projeto (API, chaves, etc.).
- `requirements.txt`: Lista todas as dependências Python necessárias.
- `src/`: Contém a lógica principal da aplicação:
  - `waha_client.py`: Funções para interagir com a API do WAHA (enviar mensagens, baixar mídias).
  - `ollama_client.py`: Funções para se comunicar com a API do Ollama.
  - `audio_processor.py`: Funções para processar e transcrever áudios com o Whisper.

## Pré-requisitos

Antes de começar, você precisará ter o seguinte instalado:

- **Python 3.8+**
- **Ollama:** Siga as instruções de instalação em [ollama.ai](https://ollama.ai/).
- **WAHA (WhatsApp HTTP API):** Você precisa ter uma instância do WAHA rodando. Veja a documentação em [devlike.pro/waha](https://devlike.pro/waha/).

## Como Configurar e Rodar

1. **Clone o Repositório:**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Instale as Dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure as Variáveis de Ambiente:**

   Crie um arquivo `.env` na raiz do projeto ou configure as variáveis de ambiente no seu sistema. As configurações principais estão em `config.py`.

   Exemplo de `.env`:
   ```
   OLLAMA_API_URL=http://localhost:11434/api/generate
   MODEL_NAME=qwen2.5:3b
   WAHA_API_URL=http://seu-ip-do-waha:3000
   WAHA_API_KEY=sua-chave-secreta-do-waha
   WHISPER_MODEL_SIZE=base
   ```

4. **Inicie o Servidor:**
   ```bash
   python app.py
   ```

   O servidor estará rodando em `http://0.0.0.0:5001` por padrão.

5. **Configure o Webhook no WAHA:**

   No seu painel do WAHA, configure o webhook para apontar para o endereço do seu servidor, no endpoint `/webhook`.

   Exemplo: `http://seu-ip-publico:5001/webhook`

## Como Usar

- **Texto:** Envie qualquer mensagem de texto para o número de WhatsApp conectado.
- **Áudio:** Envie uma mensagem de áudio ou uma nota de voz. A IA irá transcrevê-la, enviar a transcrição e depois responder ao texto transcrito.
