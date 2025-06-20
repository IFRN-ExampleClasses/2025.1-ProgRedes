import socket, sys, ssl

# --------------------------------------------------
# Constantes do Programa
PORT_HTTP = 80
PORT_HTTPS = 443
CODE_PAGE = 'utf-8'
BUFFER_SIZE = 4096

# Templates de requisição
REQ_HEAD_TEMPLATE = 'HEAD /{} HTTP/1.1\r\nHost: {}\r\nAccept: text/html\r\nConnection: close\r\n\r\n'
REQ_GET_TEMPLATE  = 'GET /{} HTTP/1.1\r\nHost: {}\r\nAccept: text/html\r\nConnection: close\r\n\r\n'
# --------------------------------------------------

strHost  = 'www.httpwatch.com'
strImage = '/httpgallery/chunked/chunkedimage.aspx'

context  = ssl.create_default_context()
sockTCP  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockSSL = context.wrap_socket(sockTCP, server_hostname=strHost)

try:
   sockSSL.connect((strHost, PORT_HTTPS))
except:
   print('1')
   sys.exit(f'\nERRO.... {sys.exc_info()[0]}')
else:
   strRequisicao = f'GET {strImage} HTTP/1.1\r\nHOST: {strHost}\r\n\r\n' 
   try:
      sockSSL.sendall(strRequisicao.encode())
   except:
      print('2')
      sys.exit(f'\nERRO.... {sys.exc_info()[0]}')
   else:
      print('-'*50)
      while True:
         strResposta = sockSSL.recv(BUFFER_SIZE)
         if not strResposta: break
         print(strResposta, '\n\n')
      print('-'*50)
      sockSSL.close()