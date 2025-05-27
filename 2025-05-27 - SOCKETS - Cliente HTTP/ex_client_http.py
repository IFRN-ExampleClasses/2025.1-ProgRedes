'''
   Este exemplo solicita um HOST ou uma URL e obtem o cabeçalho 
   e o conteúdo da resposta da requisição seguindo o padrão do 
   protocolo HTTP


   - Documentação Protocolo HTTP
        https://developer.mozilla.org/pt-BR/docs/Web/HTTP
        https://datatracker.ietf.org/doc/html/rfc9110
        https://datatracker.ietf.org/doc/html/rfc7540

   - Status Code (Códigos de Resposta HTTP)
        https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status
   
   - Headers (Cabeçalhos HTTP)
        https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Headers

   - Conexão Socket SSL
        https://docs.python.org/3/library/ssl.html

'''
import socket, sys, ssl

# --------------------------------------------------
# Constantes do Programa
PORT_HTTP   = 80
PORT_HTTPS  = 443
CODE_PAGE   = 'utf-8'
BUFFER_SIZE = 1024
# --------------------------------------------------

strHost = input('\nInforme o nome do HOST ou URL do site: ')

strReqHead    = f'HEAD / HTTP/1.1\r\nHost: {strHost}\r\nAccept: text/html\r\n\r\n'
strReqContent = f'GET / HTTP/1.1\r\nHost: {strHost}\r\nAccept: text/html\r\n\r\n'

sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sockTCP.connect((strHost, PORT_HTTP))
except:
    sys.exit(f'\nERRO.... {sys.exc_info()[0]}')
else:
    try:
        sockTCP.sendall(strReqHead.encode(CODE_PAGE))
    except:
        sys.exit(f'\nERRO.... {sys.exc_info()[0]}')
    else:
        strResposta = sockTCP.recv(BUFFER_SIZE).decode(CODE_PAGE)
        strResposta = strResposta.split('\r\n')[0].split(' ')
        intStatus   = int(strResposta[1])
        
        # Conectar SOCKET(Buscar a nova URL + Porta 443)
        if intStatus >= 300 and intStatus < 400:
            context = ssl.create_default_context()
            try:
                # TODO: Obter URL -> Location no Header
                #strURL = ...
                
                # TODO: Estabelecer conexão via SSL
                #sockTCPSecure = socket.create_connection((strURL, PORT_HTTPS))
                ...        
            except:
                sys.exit(f'\nERRO.... {sys.exc_info()[0]}')
            else:
                # TODO: Apagar depois
                print('OK HTTPS')
        else:
            # TODO: Apagar depois
            print('OK HTTP')

        # TODO: Obter tamanho área conteúdo (Content-Length do Header)

        # TODO: Iniciar recebimento do conteúdo controlando pelo Content-Length

        sockTCP.close()