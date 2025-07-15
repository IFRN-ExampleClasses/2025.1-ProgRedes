# bot_funcoes.py

from pynput import keyboard
import math
import os
import requests

strDirApp = os.path.dirname(__file__)
strDirImg = f'{strDirApp}/imagens'
strDirArq = f'{strDirApp}/arquivos'

# ------------------------------------------------------------------------------------------
# Função para detectar F10 - Interrompe o listener
def getKey(key):
   if key == keyboard.Key.f10:
      print('\n<F10> pressionado. Encerrando o bot...')
      return False

# ------------------------------------------------------------------------------------------
# Função para exibir a lista de comandos disponíveis
def exibeAjuda() -> str:
    return 'Comandos disponíveis:\n' \
           '/? - Exibe esta mensagem de ajuda\n' \
           '/fat:n - Calcula o fatorial de n (exemplo: /fat:5)\n' \
           '/fib:n - Exibe os n primeiros elementos da sequência de Fibonacci (exemplo: /fib:10)\n' \
           '/img:nome_arquivo - Envia o arquivo nome_arquivo do servidor para o Telegram (exemplo: /img:foto.jpg)'

# ------------------------------------------------------------------------------------------
# Função para exibir mensagem de boas-vindas
def exibeBoasVindas() -> str:
    return 'Olá! Bem-vindo ao bot. 😊\n' \
           'Use /? para ver os comandos disponíveis.'

# ------------------------------------------------------------------------------------------
# Função para calcular o fatorial de n
def calculaFatorial(valor: int = None) -> str:
   if valor is None:
      return 'ERRO: O comando /fat requer um argumento. Exemplo: /fat:5'
   
   try:
      intValor = int(valor)
      if intValor < 0:
         return 'ERRO: O fatorial é definido apenas para números inteiros não negativos.'
      if intValor > 1000:
         return 'ERRO: O valor de n é muito grande (limite: 1000).'
      return f'Fatorial de {intValor}: {math.factorial(intValor)}'
   except ValueError:
      return 'ERRO: O valor de n deve ser um número inteiro.'
   except Exception as e:
      return f'ERRO: {e}'

# ------------------------------------------------------------------------------------------
# Função para exibir os n primeiros elementos da sequência de Fibonacci
def exibeFibonacci(valor: int = None) -> str:
   if valor is None:
      return 'ERRO: O comando /fib requer um argumento. Exemplo: /fib:10'
   
   try:
      intValor = int(valor)
      if intValor <= 0:
         return 'ERRO: O valor de n deve ser maior que zero.'
      if intValor > 1000:
         return 'ERRO: O valor de n é muito grande (limite: 1000).'
      fib = [1, 1]  # Sequência de Fibonacci começa com 1 e 1
      for _ in range(2, intValor):
         fib.append(fib[-1] + fib[-2])
      return f'Os {intValor} primeiros elementos da sequência de Fibonacci são:\n{", ".join(map(str, fib[:intValor]))}'
   except ValueError:
      return 'ERRO: O valor de n deve ser um número inteiro.'
   except Exception as e:
      return f'ERRO: {e}'

# ------------------------------------------------------------------------------------------
# Função para enviar arquivos para o Telegram
def enviarImagem(nome_arquivo: str, chat_id: int, strURLSendImage: str, logger) -> str:
    try:
        # Verifica se o diretório de imagens existe
        if not os.path.exists(strDirImg):
            return f'ERRO: O diretório de imagens "{strDirImg}" não foi encontrado.'

        # Caminho completo do arquivo
        strNomeArquivo = f'{strDirImg}/{nome_arquivo}'

        # Verifica se o arquivo existe
        if not os.path.exists(strNomeArquivo):
            return f'ERRO: O arquivo {nome_arquivo} não foi encontrado.'

        # Envia a imagem usando a API do Telegram
        with open(strNomeArquivo, 'rb') as file:
            files = {'photo': file}  # Arquivo de imagem
            data = {'chat_id': chat_id}  # Dados adicionais (chat_id)
            response = requests.post(strURLSendImage, files=files, data=data)

        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            return f'AVISO: Arquivo {nome_arquivo} enviado com sucesso!'
        else:
            # Log do erro completo
            strMsgErro = f'ERRO: Falha ao enviar o arquivo. Código de retorno: {response.status_code}\nResposta: {response.text}'
            logger.error(strMsgErro)
            return strMsgErro
    except Exception as e:
        strMsgErro = f'ERRO: Erro ao enviar imagem: {e}'
        logger.error(strMsgErro)
        return strMsgErro

# ------------------------------------------------------------------------------------------
# Função para processar mensagens
def processar_mensagem(message, strURLSendMessage: str, strURLSendImage: str, logger):
    try:
        strComando = message.get('text', '')
        intIDChat = message['chat']['id']

        # Verifica se o texto começa com '/'
        if strComando.startswith('/'):
            lstPartes = strComando.split(':')
            strComando = lstPartes[0]
            strParametro = lstPartes[1] if len(lstPartes) > 1 else None

            # Verifica se o comando está no dicionário de comandos
            if strComando in dictComandos.keys():
                if strParametro:
                    # Chama a função correspondente ao comando com os parâmetros corretos
                    if strComando == '/img':
                        strMensagemRetorno = f'BOT: {dictComandos[strComando](strParametro, intIDChat, strURLSendImage, logger)}\nUsuário: {intIDChat}'
                    else:
                        strMensagemRetorno = f'BOT: {dictComandos[strComando](strParametro)}\nUsuário: {intIDChat}'
                else:
                    # Comando sem parâmetro
                    strMensagemRetorno = f'BOT: {dictComandos[strComando]()}\nUsuário: {intIDChat}'
            else:
                # Comando não reconhecido
                strMensagemRetorno = f'BOT: Comando não reconhecido...\nUsuário: {intIDChat}'
        else:
            # Mensagem que não começa com '/'
            strMensagemRetorno = f'BOT: Não é um comando válido.\nOs comandos devem começar com /...\nUsuário: {intIDChat}'

        # Envia a mensagem de retorno
        dictDados = {'chat_id': intIDChat, 'text': strMensagemRetorno}
        reqURL = requests.post(strURLSendMessage, data=dictDados)

        # Verifica se a requisição foi bem sucedida
        if not reqURL.status_code == 200:
            logger.error(f'ERRO: Erro ao enviar mensagem: {reqURL.status_code}')
    except Exception as e:
        logger.error(f'ERRO: Erro ao processar mensagem: {e}')

# ------------------------------------------------------------------------------------------
# Dicionário de comandos
dictComandos = {
   '/?': exibeAjuda,
   '/fat': lambda n=None: calculaFatorial(n),
   '/fib': lambda n=None: exibeFibonacci(n),
   '/img': lambda n, chat_id, strURLSendImage, logger: enviarImagem(n, chat_id, strURLSendImage, logger),  # Passa o chat_id, strURLSendImage e logger como parâmetros
}