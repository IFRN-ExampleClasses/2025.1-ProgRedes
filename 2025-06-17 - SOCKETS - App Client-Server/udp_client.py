import socket

from constantes import *

# Criando o socket (socket.AF_INET -> IPV4 / socket.SOCK_DGRAM -> UDP)
sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print('\n\nPara sair use EXIT...\n\n')

while True:
   # Informando a mensagem a ser enviada para o servidor
   strMensagem = input('Digite a mensagem: ')

   # Saindo do Cliente quando digitar EXIT
   if strMensagem.lower().strip() == 'exit': break

   # Convertendo a mensagem em bits
   bytesMensagem = strMensagem.encode(CODE_PAGE) 

   # Enviando a mensagem ao servidor      
   sockUDP.sendto(bytesMensagem, (HOST_IP_SERVER, HOST_PORT))

# Fechando o socket
sockUDP.close()
