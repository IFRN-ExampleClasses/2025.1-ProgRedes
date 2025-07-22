import os, sys, requests, platform

# Deve ser criado um arquivo com o nome token.py
# e dentro criar a "constante" API_TOKEN e
# atribuir o valor do token informado pelo Bot Father
from token import *

# URL Base de requisições da API do TELEGRAM
strURL = f'https://api.telegram.org/bot{API_TOKEN}'

# Demais URL´s da API
strURLGetUpdate = f'{strURL}/getUpdates'

# Limpando a tela
os.system('cls' if platform.system() == 'Windows' else 'clear')

print('\nBOT TELEGRAM - Aguardando mensagens...')
print('---------------------------------------\n')

#intContador = 1
while True:
   try:
      reqURL = requests.get(strURLGetUpdate)
   except Exception as erro:
      sys.exit(f'\nERRO: {erro}')
   else:
      if not reqURL.status_code == 200:
         sys.exit(f'\nERRO: Erro ao acessar a URL\nCÓDIGO DE RETORNO: {reqURL.status_code}')

      jsonRetorno = reqURL.json()

      print(jsonRetorno, '\n')