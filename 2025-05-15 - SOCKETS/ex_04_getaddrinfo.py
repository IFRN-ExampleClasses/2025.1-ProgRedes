import socket, sys

#------------------------------------------------------------
def get_protnumber(prefix):
   return dict ((getattr(socket, a), a)
      for a in dir(socket)
         if a.startswith(prefix) )
#------------------------------------------------------------

family    = get_protnumber('AF_')
types     = get_protnumber('SOCK_')
protocols = get_protnumber('IPPROTO_')

server = input('\nInforme o nome do HOST ou URL do site: ')

try:
   infos = socket.getaddrinfo(host=server, port='http')
except:
   sys.exit(f'\nERRO:Não foi possível resolver o nome do host.\n{sys.exc_info()}')
else:
   for info in infos:
      intFamily, intSocktype, intProto, strCName, sockaddr = info
      
      print('\n----------------------------------------')
      print(f'Info ...................: {info}')
      print(f'Family .................: {family[intFamily]}')
      print(f'Type ...................: {types[intSocktype]}')
      print(f'Proto ..................: {protocols[intProto]}')
      print(f'Canonical Name (CNAME) .: {strCName}')   
      print(f'SOCKET Address .........: {sockaddr}')