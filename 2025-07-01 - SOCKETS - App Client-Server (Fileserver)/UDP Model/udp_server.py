import socket

from constantes import *
from funcoes_especificas import *

# Criando o socket (socket.AF_INET -> IPV4 / socket.SOCK_DGRAM -> UDP)
sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Ligando o socket à porta
sockUDP.bind(('', HOST_PORT)) 

print('\nRecebendo Comandos...\n\n')

while True:
   # Recebendo os comandos do cliente
   byteMensagem, tuplaCliente = sockUDP.recvfrom(BUFFER_SIZE)
   strMensagem = byteMensagem.decode(CODE_PAGE).lower().strip()

   boolErro = True
   if not strMensagem.startswith('\\'):
      strMensagemRetorno = 'ERRO: Comandos iniciam com \\. Digite \\? para ajuda...'
   elif strMensagem == '\\?':
      strMensagemRetorno = getAjuda()  
   elif strMensagem.startswith('\\d:'):
      strComando, strNomeArquivo = strMensagem.split(':')
      if not strNomeArquivo:
         strMensagemRetorno = f'ERRO: Faltou informar o nome do arquivo...'
      else:
         try:
            strNomeArquivo = f'{DIR_IMG_SERVER}\\{strNomeArquivo}'
            boolSucesso = enviarArquivo(sockUDP, strNomeArquivo, tuplaCliente)
            if boolSucesso:
               print(f'AVISO: Arquivo enviado com sucesso para f{tuplaCliente}.')
               boolErro = False
         except Exception as erro:
            print(erro)
   else:
      strMensagemRetorno = 'ERRO: Comando desconhecido. Digite \\? para ajuda...'  
      
   # Enviando mensagem de retorno ao cliente
   if boolErro:   
      sockUDP.sendto(strMensagemRetorno.encode(CODE_PAGE), tuplaCliente)

# Fechando o socket
sockUDP.close()

print('\nAVISO: Servidor finalizado...\n')