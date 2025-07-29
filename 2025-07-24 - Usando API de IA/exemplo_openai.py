'''
   1) Instalar a biblioteca da OpenAI

      a) pip install openai --user

   2) Obter uma API Key da OpenAI:

      a) https://platform.openai.com

      b) Gerar sua API Key.
'''

import openai

from api_tokens import *

# ----------------------------------------------------------------------
# Criando um cliente com o modelo
clienteOpenAI = openai.OpenAI(api_key = strTokenOpenAI)

# ----------------------------------------------------------------------
def perguntarOPENAI(strPrompt: str) -> str:
   try:
      resposta = clienteOpenAI.chat.completions.create(
         model    = 'gpt-3.5-turbo',  # Ou gpt-4, se sua conta permitir
         messages = [ {'role': 'user', 'content': strPrompt}]
      )
      return resposta.choices[0].message.content.strip()
   except Exception as e:
      return f'\nERRO: {e}...'


# ----------------------------------------------------------------------
def main():
   while True:
      strTexto = input('\nDigite sua pergunta (SAIR - Encerra): ').lower()
      if strTexto == 'sair':
         print('\nSaindo do Programa...')
         break

      strResposta = perguntarOPENAI(strTexto)
      print(f'\nResposta do DEEPSEEK:\n{strResposta}')

# ----------------------------------------------------------------------
if __name__ == '__main__':
   main()
