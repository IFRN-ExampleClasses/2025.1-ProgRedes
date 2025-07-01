import socket

from constantes import *

# Criando o socket (socket.AF_INET -> IPV4 / socket.SOCK_DGRAM -> UDP)
sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Ligando o socket à porta
sockUDP.bind(('', HOST_PORT)) 

print('\nRecebendo Mensagens...\n\n')

while True:
    # Recebendo os dados do cliente
    byteMensagem, tuplaCliente = sockUDP.recvfrom(BUFFER_SIZE)

    # Imprimindo a mensagem recebida convertendo de bytes para string
    print(f'{tuplaCliente}: {byteMensagem.decode(CODE_PAGE)}')

    # Enviando mensagem de retorno (ECHO) ao cliente
    strECHO = f'DEVOLVENDO: {byteMensagem.decode(CODE_PAGE)}'
    sockUDP.sendto(strECHO.encode(CODE_PAGE), tuplaCliente)

# Fechando o socket
sockUDP.close()

print('\nAVISO: Servidor finalizado...\n')