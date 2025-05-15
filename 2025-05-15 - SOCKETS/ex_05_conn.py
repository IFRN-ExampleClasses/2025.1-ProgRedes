import socket, sys

strHost = input('\nInforme o nome do HOST ou URL do site: ')
intPort = 22

try:
   strIPHost = socket.gethostbyname(strHost)
except:
   sys.exit(f'\nERRO: Não foi possível resolver o nome do host.\n{sys.exc_info()}')
else:
   socketTeste = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      socketTeste.connect((strIPHost, intPort))
   except:
      print(f'\nERRO: {sys.exc_info()}')
   else:
      print('\nConexão OK')
      socketTeste.close()