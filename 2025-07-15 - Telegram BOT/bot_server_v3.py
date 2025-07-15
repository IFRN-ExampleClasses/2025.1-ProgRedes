# bot_telegram.py

import os
import sys
import requests
import platform
import logging
from pynput import keyboard
from bot_funcoes import dictComandos, exibeBoasVindas, getKey, processar_mensagem

# ----------------------------------------------------------------------
# Configuração do Logging (apenas para arquivo)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_telegram.log')  # Salva logs em um arquivo
    ]
)
logger = logging.getLogger(__name__)

# Define o token do Bot (recomendado usar variáveis de ambiente)
API_TOKEN = '5671451820:AAH9qmCpnza1vQ0pdoDq97-KMg9vopihQys'

# URLs de requisição
strURLBase        = f'https://api.telegram.org/bot{API_TOKEN}'
strURLGetUpdates  = f'{strURLBase}/getUpdates'
strURLSendMessage = f'{strURLBase}/sendMessage'
strURLSendImage   = f'{strURLBase}/sendPhoto' 

# ----------------------------------------------------------------------
# Inicialização do Bot

# Limpa a tela
os.system('cls' if platform.system() == 'Windows' else 'clear')

# Exibe mensagens de inicialização na tela (usando print)
print('\nBOT TELEGRAM - Aguardando mensagens...')
print('Pressione <F10> para encerrar o bot....')
print('---------------------------------------\n')

# Inicializa a variável de controle do offset
intOffset = 0

# Inicia o listener para detectar F10
listener = keyboard.Listener(on_press=getKey)
listener.start()

# Loop principal do bot
while True:
    # Verifica se o listener ainda está ativo
    if not listener.is_alive():
        logger.info('Listener encerrado. Finalizando o bot...')
        break

    # Obtém as mensagens com o offset atual
    dictParametros = {'offset': intOffset, 'timeout': 10}  # timeout de 10 segundos
    reqURL = requests.get(strURLGetUpdates, params=dictParametros)

    # Verifica se a requisição foi bem sucedida
    if not reqURL.status_code == 200:
        strMsgErro = f'\nERRO: Erro ao obter mensagem...\nCÓDIGO DE RETORNO: {reqURL.status_code}'
        logger.error(strMsgErro)
        sys.exit(strMsgErro)

    # Converte a resposta para JSON
    jsonRetorno = reqURL.json()

    # Verifica se há novas mensagens
    if not jsonRetorno['result']: continue

    # Processa cada atualização recebida
    for update in jsonRetorno['result']:
        # Atualiza o offset para a próxima requisição
        intOffset = update['update_id'] + 1

        # Verifica se é uma atualização de status do chat (usuário entrou no bot)
        if 'my_chat_member' in update:
            chat_member = update['my_chat_member']
            if chat_member['new_chat_member']['status'] == 'member':
                intIDChat = chat_member['chat']['id']
                strMensagemRetorno = f'BOT: {exibeBoasVindas()}\nUsuário: {intIDChat}'
                dictDados = {'chat_id': intIDChat, 'text': strMensagemRetorno}
                requests.post(strURLSendMessage, data=dictDados)

        # Verifica se é uma mensagem de texto
        if 'message' in update:
            logger.info(f'Mensagem recebida: {update['message']}')
            processar_mensagem(update['message'], strURLSendMessage, strURLSendImage, logger)

# Envia a mensagem de retorno - BOT Off-line
strMensagemRetorno = f'BOT: Off-line...\nUsuário: {intIDChat}'
dictDados = {'chat_id': intIDChat, 'text': strMensagemRetorno}
reqURL = requests.post(strURLSendMessage, data=dictDados)

# Encerra o listener
listener.stop()