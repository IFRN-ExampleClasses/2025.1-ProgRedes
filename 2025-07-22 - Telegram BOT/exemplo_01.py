import os, sys, requests, platform

# Deve ser criado um arquivo com o nome token.py
# e dentro criar a "constante" API_TOKEN e
# atribuir o valor do token informado pelo Bot Father
from token_bot import *

# URL Base de requisições da API do TELEGRAM
strURLBase = f'https://api.telegram.org/bot{API_TOKEN}'

# Demais URL´s da API
strURLGetUpdate   = f'{strURLBase}/getUpdates'
strURLSendMessage = f'{strURLBase}/sendMessage'
strURLSendImage   = f'{strURLBase}/sendPhoto'

# Limpando a tela
os.system('cls' if platform.system() == 'Windows' else 'clear')

print('\nBOT TELEGRAM - Aguardando mensagens...')
print('---------------------------------------\n')

# Inicializa a variável de controle do ID da última mensagem
intIDUltimaMensagem = 0

while True:
   try:
      reqURL = requests.get(strURLGetUpdate)
   except KeyboardInterrupt:
      sys.exit('\nAVISO: Saindo do Programa...')
   except Exception as erro:
      sys.exit(f'\nERRO: {erro}...')
   else:
      if not reqURL.status_code == 200:
         sys.exit(f'\nERRO: Erro ao acessar a URL\nCÓDIGO DE RETORNO: {reqURL.status_code}')

      # Obtendo todas as mensagens que chegam ao Bot 
      jsonRetorno = reqURL.json()

      # Obtém o ID da última mensagem
      intIDMensagem = jsonRetorno['result'][-1]['message']['message_id']

      # Verifica se a última mensagem é a mesma
      if intIDMensagem == intIDUltimaMensagem: continue

      # Atualiza o ID da última mensagem
      intIDUltimaMensagem = intIDMensagem

      # Extraindo apenas a última mensagem do Bot
      strMensagem = jsonRetorno['result'][-1]['message']

      print(f'{strMensagem}\n')