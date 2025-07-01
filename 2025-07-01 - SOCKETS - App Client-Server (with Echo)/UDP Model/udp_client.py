import socket

from constantes import *

# Criando o socket (socket.AF_INET -> IPV4 / socket.SOCK_DGRAM -> UDP)
sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print('\n\nPara sair digite EXIT...\n\n')

while True:
   # Informando a mensagem a ser enviada para o servidor
   strMensagem = input('Digite a mensagem: ')

   # Saindo do Cliente quando digitar EXIT
   if strMensagem.lower().strip() == 'exit': break

   # Enviando a mensagem ao servidor      
   sockUDP.sendto(strMensagem.encode(CODE_PAGE), (HOST_IP_SERVER, HOST_PORT))

   # Recebendo ECHO do servidor
   byteRetorno, tuplaRetorno = sockUDP.recvfrom(BUFFER_SIZE)
   print (f'ECHO RECEBIDO {tuplaRetorno}: {byteRetorno.decode(CODE_PAGE)} ')

# Fechando o socket
sockUDP.close()
