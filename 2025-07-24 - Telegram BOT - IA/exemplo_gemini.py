'''
   1) Instalar a biblioteca do Gemini

      a) pip install google-generativeai

   2) Obter uma API Key do Google AI:

      a) Acessar: https://makersuite.google.com/app/apikey

      b) Gerar e copiar a chave da API.
'''

import google.generativeai as genai

from token_api import *

# ----------------------------------------------------------------------
# Colocando a chave da API
genai.configure(api_key=strTokenGemini)

# Criando  uma instância do modelo Gemini
modGemini = genai.GenerativeModel('gemini-1.5-flash')

# ----------------------------------------------------------------------
def perguntarGEMINI(strPrompt: str) -> str:
    try:
        strRetorno = modGemini.generate_content(strPrompt)
        return strRetorno.text.strip()
    except Exception as e:
        return f'\nERRO - GEMINI: {e}'


# ----------------------------------------------------------------------
def main():
   while True:
      strTexto = input('\nDigite sua pergunta (SAIR - Encerra): ').lower()
      if strTexto == 'sair':
         print('\nSaindo do Programa...')
         break

      strResposta = perguntarGEMINI(strTexto)
      print(f'\nResposta do GEMINI:\n{strResposta}')

# ----------------------------------------------------------------------
if __name__ == '__main__':
   main()
