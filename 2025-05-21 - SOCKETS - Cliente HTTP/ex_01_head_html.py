'''
   Este exemplo solicita um HOST ou uma URL e obtem o cabeçalho de
   resposta da requisição seguindo o padrão do protocolo HTTP


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

strHost = input('\nInforme o nome do HOST ou URL do site: ')

sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sockTCP.connect((strHost, PORT))
except:
    sys.exit(f'\nERRO.... {sys.exc_info()[0]}')
else:
    strRequisicao = f'HEAD / HTTP/1.1\r\nHost: {strHost}\r\nAccept: text/html\r\n\r\n'
    try:
        sockTCP.sendall(strRequisicao.encode(CODE_PAGE))
    except:
        sys.exit(f'\nERRO.... {sys.exc_info()[0]}')
    else:
        strResposta = sockTCP.recv(BUFFER_SIZE).decode(CODE_PAGE)
        print('-'*50)
        print(strResposta)
        print('-'*50)
        sockTCP.close()