import socket

#------------------------------------------------------------
def get_protnumber(prefix):
   return dict ((getattr(socket, a), a)
      for a in dir(socket)
         if a.startswith(prefix) )
#------------------------------------------------------------

socketsFamily    = get_protnumber('AF_')
socketsTypes     = get_protnumber('SOCK_')
socketsProtocols = get_protnumber('IPPROTO_')

socketsFamily    = {k: v for k, v in sorted(socketsFamily.items(), key=lambda item: int(item[0]))}
socketsTypes     = {k: v for k, v in sorted(socketsTypes.items(), key=lambda item: int(item[0]))}
socketsProtocols = {k: v for k, v in sorted(socketsProtocols.items(), key=lambda item: int(item[0]))}

print('\nFamílias de Sockets:')
for k,v in socketsFamily.items(): print(f'{k:02d} - {v}')

print('\n\nTipos de Sockets:')
for k,v in socketsTypes.items(): print(f'{k:02d} - {v}')

print('\n\nProtocolos de Sockets:')
for k,v in socketsProtocols.items(): print(f'{k:03d} - {v}')

