import socket

# ----------------------------------------------------------------------
HOST_IP_SERVER    = ''              # Definindo o IP do servidor
HOST_PORT         = 50000           # Definindo a porta

CODE_PAGE         = 'utf-8'         # Definindo a página de caracteres
BUFFER_SIZE       = 512             # Tamanho do buffer
# ----------------------------------------------------------------------

# Criando o socket (socket.AF_INET -> IPV4 / socket.SOCK_DGRAM -> UDP)
sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Ligando o socket à porta
sockUDP.bind((HOST_IP_SERVER, HOST_PORT)) 

print('\nRecebendo Mensagens...\n\n')

while True:
    # Recebendo os dados do cliente
    byteMensagem, tuplaCliente = sockUDP.recvfrom(BUFFER_SIZE)
    
    # Imprimindo a mensagem recebida convertendo de bytes para string
    print(f'{tuplaCliente}: {byteMensagem.decode(CODE_PAGE)}')

# Fechando o socket
sockUDP.close()

print('\nAVISO: Servidor finalizado...')
