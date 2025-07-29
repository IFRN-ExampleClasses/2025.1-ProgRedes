'''
   1) Obter uma API Key da DeepSeek Cloud:

      a) https://platform.deepseek.com

      b) Criar uma conta e gere sua API Key.
'''

import requests

from api_tokens import *

# ----------------------------------------------------------------------
# Definindo os parêmtros iniciais da API do DeepSeek
API_KEY = strTokenDeepseek
API_URL = 'https://api.deepseek.com/v1/chat/completions'

HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# ----------------------------------------------------------------------
def perguntarDEEPSEEK(strPrompt: str) -> str:
   try:
      payload = {
         'model'      : 'deepseek-chat',  # ou 'deepseek-coder' se preferir
         'messages'   : [ {'role': 'user', 'content': strPrompt} ],
         'temperature': 0.7
      }

      reqEnvio = requests.post(API_URL, headers=HEADERS, json=payload)
      reqEnvio.raise_for_status()
      data = reqEnvio.json()
      return data['choices'][0]['message']['content'].strip()

   except Exception as e:
      return f'\nERRO: {e}...'


# ----------------------------------------------------------------------
def main():
   while True:
      strTexto = input('\nDigite sua pergunta (SAIR - Encerra): ').lower()
      if strTexto == 'sair':
         print('\nSaindo do Programa...')
         break

      strResposta = perguntarDEEPSEEK(strTexto)
      print(f'\nResposta do DEEPSEEK:\n{strResposta}')

# ----------------------------------------------------------------------
if __name__ == '__main__':
   main()
