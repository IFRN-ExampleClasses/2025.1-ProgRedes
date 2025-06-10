'''
   Este exemplo define uma variavel de HOST e uma variavel de
   IMAGE e obtem o cabeçalho de resposta da requisição (imagem)
   seguindo o padrão do protocolo HTTP


   - Documentação Protocolo HTTP
        https://developer.mozilla.org/pt-BR/docs/Web/HTTP
        https://datatracker.ietf.org/doc/html/rfc9110
        https://datatracker.ietf.org/doc/html/rfc7540

   - Status Code (Códigos de Resposta HTTP)
        https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status
   
   - Headers (Cabeçalhos HTTP)
        https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Headers
'''
import socket, sys

# --------------------------------------------------
# Constantes do Programa
PORT        = 80
CODE_PAGE   = 'utf-8'
BUFFER_SIZE = 1024
# --------------------------------------------------

#strHost  = 'www.httpbin.org'
#strImage = '/image/webp'


strHost = 'wallpapers.com'
strImage = '/images/high/4k-star-wars-the-last-jedi-660ztmpvnlox8hlm.webp'
sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
   sockTCP.connect((strHost, PORT))
except:
    sys.exit(f'\nERRO.... {sys.exc_info()[0]}')
else:
   strRequisicao = f'HEAD /{strImage} HTTP/1.1\r\nHOST: {strHost}\r\n\r\n' 
   try:
      sockTCP.sendall(strRequisicao.encode())
   except:
      sys.exit(f'\nERRO.... {sys.exc_info()[0]}')
   else:
      strResposta = sockTCP.recv(BUFFER_SIZE).decode(CODE_PAGE)
      print('-'*50)
      print(strResposta)
      print('-'*50)
      sockTCP.close()