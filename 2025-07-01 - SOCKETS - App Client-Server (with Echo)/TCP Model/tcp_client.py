import socket

from constantes import *

# Criando o socket (socket.AF_INET -> IPV4 / socket.SOCK_STREAM -> TCP)
sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectando ao servidor
sockTCP.connect((HOST_IP_SERVER, HOST_PORT))

print('\n\nPara sair digite EXIT...\n\n')

try:
   while True:
      # Informando a mensagem a ser enviada para o servidor
      strMensagem = input('Digite a mensagem: ').strip()

      # Saindo do Cliente quando digitar EXIT
      if strMensagem.lower() == 'exit': break

      # Enviando a mensagem ao servidor      
      sockTCP.send(strMensagem.encode(CODE_PAGE) )

      # Recebendo echo do servidor
      strECHO = sockTCP.recv(BUFFER_SIZE).decode(CODE_PAGE)
      print (f'ECHO RECEBIDO: {strECHO} ')
except KeyboardInterrupt:
   print('\nCTRL+C pressionado.')
except Exception as e:
   print(f'ERRO: {e}')
finally:
   # Fechando o socket
   sockTCP.close()
   print('Cliente finalizado com segurança.')
