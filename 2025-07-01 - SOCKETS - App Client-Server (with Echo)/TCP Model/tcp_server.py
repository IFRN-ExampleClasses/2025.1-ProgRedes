import socket

from constantes import *

# Criando o socket (socket.AF_INET -> IPV4 / socket.SOCK_STREAM -> TCP)
sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ligando o socket à porta
sockTCP.bind((HOST_IP_SERVER, HOST_PORT)) 

# Tornando o socket capaz de escutar conexões - Tamanho da fila de conexões pendentes
sockTCP.listen(5)

print('\nServidor Recebendo Mensagens...\n\n')

try:
   while True:
      # Aceitando uma conexão de cliente
      connConexao, tuplaCliente = sockTCP.accept()
      print(f'Conexão estabelecida com {tuplaCliente}')

      while True:
        try:
           # Recebendo dados do cliente
           strMensagem = connConexao.recv(1024).decode(CODE_PAGE)
           print(f'{tuplaCliente}: {strMensagem}')

           # Enviando mensagem de retorno (ECHO) ao cliente
           strECHO = f'DEVOLVENDO: {strMensagem}'
           connConexao.send(strECHO.encode(CODE_PAGE))
        except (ConnectionResetError, ConnectionAbortedError):
           print(f'Conexão com {tuplaCliente} foi encerrada abruptamente...')
           break
except KeyboardInterrupt:
   print('\nServidor interrompido pelo usuário.')
finally:
   # Fechando o socket
   sockTCP.close()
   print('Socket do servidor fechado. Servidor finalizado com segurança.')
