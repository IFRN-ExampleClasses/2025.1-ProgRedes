import os, sys, requests, platform

API_TOKEN = 'YOUR_TOKEN_HERE'

strURL = f'https://api.telegram.org/bot{API_TOKEN}'

os.system('cls' if platform.system() == 'Windows' else 'clear')
print('\nBOT TELEGRAM - Aguardando mensagens...')
print('---------------------------------------\n')

intContador = 1
while True:

   reqURL = requests.get(strURL + '/getUpdates')

   if not reqURL.status_code == 200:
      sys.exit('\nERRO: Erro ao acessar a URL\nCÓDIGO DE RETORNO: ' + str(reqURL.status_code))

   jsonRetorno = reqURL.json()
   strMensagem = jsonRetorno['result'][-1]['message']['text']

   print('REQUISIÇÃO Nº: ' + str(intContador))
   print(f'{strMensagem}')
   print('-'*100+'\n')
   intContador += 1