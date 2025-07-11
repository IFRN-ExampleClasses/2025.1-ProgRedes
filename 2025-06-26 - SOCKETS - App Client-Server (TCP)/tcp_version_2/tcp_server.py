import socket

from constantes import *

# Criando o socket (socket.AF_INET -> IPV4 / socket.SOCK_STREAM -> TCP)
sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ligando o socket à porta
sockTCP.bind((HOST_IP_SERVER, HOST_PORT)) 

# Tornando o socket capaz de escutar conexões - Tamanho da fila de conexões pendentes
sockTCP.listen(5)

print('\nRecebendo Mensagens...\n\n')

while True:
    # Aceitando uma conexão de cliente
    connConexao, tuplaCliente = sockTCP.accept()
    
    # Exibindo a tupla (IP, PORTA) do cliente conectado
    print(f'Conexão estabelecida com {tuplaCliente}')

    # Recebendo dados do cliente
    byteMensagem = connConexao.recv(1024)

    # Imprimindo a mensagem recebida convertendo de bytes para string
    print(f'{tuplaCliente}: {byteMensagem.decode(CODE_PAGE)}')

# Fechando o socket
sockTCP.close()

print('\nAVISO: Servidor finalizado...')
