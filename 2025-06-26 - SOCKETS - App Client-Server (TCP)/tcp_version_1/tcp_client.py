import socket

# ----------------------------------------------------------------------
HOST_IP_SERVER    = '10.27.1.238'   # Definindo o IP do servidor
HOST_PORT         = 50000           # Definindo a porta

CODE_PAGE         = 'utf-8'         # Definindo a página de caracteres
BUFFER_SIZE       = 512             # Tamanho do buffer
# ----------------------------------------------------------------------

# Criando o socket (socket.AF_INET -> IPV4 / socket.SOCK_STREAM -> TCP)
sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectando ao servidor
sockTCP.connect((HOST_IP_SERVER, HOST_PORT))

print('\n\nPara sair digite EXIT...\n\n')

while True:
   # Informando a mensagem a ser enviada para o servidor
   strMensagem = input('Digite a mensagem: ')

   # Saindo do Cliente quando digitar EXIT
   if strMensagem.lower().strip() == 'exit': break

   # Convertendo a mensagem em bits
   bytesMensagem = strMensagem.encode(CODE_PAGE) 

   # Enviando a mensagem ao servidor      
   sockTCP.send(bytesMensagem)

# Fechando o socket
sockTCP.close()
