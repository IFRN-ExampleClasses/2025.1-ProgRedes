import socket

from constantes import *

# Garantindo que a pasta de recepção de arquivos exista
os.makedirs(DIR_IMG_CLIENT, exist_ok=True)

# Criando o socket (socket.AF_INET -> IPV4 / socket.SOCK_DGRAM -> UDP)
sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print('\n\nPara sair digite EXIT (/? -> Ajuda)...\n\n')

while True:
   # Informando a mensagem a ser enviada para o servidor
   strMensagem = input('Digite o comando: ').lower().strip()

   # Saindo do Cliente quando digitar EXIT
   if strMensagem == 'exit': break

   # Enviando a mensagem ao servidor      
   sockUDP.sendto(strMensagem.encode(CODE_PAGE), (HOST_IP_SERVER, HOST_PORT))

   # Recebendo resposta inicial do servidor (pode ser erro ou cabeçalho)
   byteRetorno, tuplaRetorno = sockUDP.recvfrom(BUFFER_SIZE)
   strRetorno = byteRetorno.decode(CODE_PAGE)   

   # Verifica se é o cabeçalho de um arquivo
   if '|' in strRetorno and not strRetorno.lower().startswith('erro'):
      strNomeArquivo, strTamanho = strRetorno.split('|')
      intTamanho = int(strTamanho)

      print(f'Recebendo arquivo \'{strNomeArquivo}\' com {intTamanho} bytes...')

      intBytesRecebidos = 0
      arqArquivoRecebe = open(f'{DIR_IMG_CLIENT}\\{strNomeArquivo}', 'wb') 
      while intBytesRecebidos < intTamanho:
         bytesRetorno, _ = sockUDP.recvfrom(BUFFER_SIZE)
         arqArquivoRecebe.write(bytesRetorno)
         intBytesRecebidos += len(bytesRetorno)

      print(f'Arquivo \'{strNomeArquivo.upper()}\' recebido com sucesso e salvo em \'{DIR_IMG_CLIENT.upper()}\'.')

   else:
      # Caso não seja transferência de arquivo, exibe mensagem do servidor
      print(strRetorno)   

# Fechando o socket
sockUDP.close()
