import socket

from constantes import *

# Criando o socket (socket.AF_INET -> IPV4 / socket.SOCK_DGRAM -> UDP)
sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Ligando o socket à porta
sockUDP.bind((HOST_IP_LOCAL, HOST_PORT)) 

print('\nRecebendo Mensagens...\n\n')

try:
    while True:
        # Recebendo os dados do cliente
        byteMensagem, tuplaCliente = sockUDP.recvfrom(BUFFER_SIZE)
        
        # Imprimindo a mensagem recebida convertendo de bytes para string
        print(f'{tuplaCliente}: {byteMensagem.decode(CODE_PAGE)}')

except KeyboardInterrupt:
    print("\nServidor interrompido pelo usuário.")

finally:
    # Fechando o socket
    sockUDP.close()
    print("Socket fechado.")
