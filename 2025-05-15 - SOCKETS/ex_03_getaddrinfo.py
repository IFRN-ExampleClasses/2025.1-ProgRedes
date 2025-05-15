import socket, sys

strHost = input('\nInforme o nome do HOST ou URL do site: ')

try:
   lstInfoHost = socket.getaddrinfo(host=strHost, port=22)
except:
   print(f'ERRO: {sys.exc_info()}')
else:
   for info in lstInfoHost:
      print('\n'+'-'*80)
      print(f'Info ...................: {info}')
      print(f'Family .................: {info[0]}')
      print(f'Type ...................: {info[1]}')
      print(f'Proto ..................: {info[2]}')
      print(f'Canonical Name (CNAME) .: {info[3]}')   
      print(f'SOCKET Address .........: {info[4]}')
