'''
   Obter o IP a partir de um host informado
'''
import socket, sys

strHost = input('\nInforme o nome do HOST ou URL do site: ')

try:
   strIPHost = socket.gethostbyname(strHost)
except socket.gaierror:
   print('ERRO: Resolução do nome está falhando para o domínio fornecido.')
except:
   print(f'ERRO: {sys.exc_info()}')
else:
   print(strIPHost)