'''
   Este exemplo solicita um HOST ou uma URL e obtem o cabeçalho 
   e o conteúdo da resposta da requisição seguindo o padrão do 
   protocolo HTTP
'''
import socket, sys, os, ssl

# --------------------------------------------------
# Constantes do Programa
PORT_HTTP   = 80
PORT_HTTPS  = 443
CODE_PAGE   = 'utf-8'
BUFFER_SIZE = 1024

DIR_APP = os.path.dirname(__file__)
# --------------------------------------------------

# Solicitando o host ao usuário
strHost = input('\nInforme o nome do HOST ou URL do site: ')

# Variáveis com as strings de requição (HEAD e GET)
strReqHead    = f'HEAD / HTTP/1.1\r\nHost: {strHost}\r\nAccept: text/html\r\n\r\n'
strReqContent = f'GET / HTTP/1.1\r\nHost: {strHost}\r\nAccept: text/html\r\n\r\n'

# Criando o Socket (AF_INET -> IPV4 / SOCK_STREAM -> TCP)
sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Conecta o socket ao (host, porta)
    sockTCP.connect((strHost, PORT_HTTP))
except:
    sys.exit(f'\nERRO.... {sys.exc_info()[0]}\n{sys.exc_info()[1]}')
else:
    try:
        # Requisita o Header
        sockTCP.sendall(strReqHead.encode(CODE_PAGE))
        # Porta que Obteve resposta 200
        intPorta = PORT_HTTP
    except:
        sys.exit(f'\nERRO.... {sys.exc_info()[0]}')
    else:
        # Obtém o Header da Requisição
        strRespHeader  = sockTCP.recv(BUFFER_SIZE).decode(CODE_PAGE)
        
        # Obtém o Status Code da requisição
        strStatusLine = strRespHeader.split('\r\n')[0]
        intStatusCode = int(strStatusLine.split(' ')[1]) if 'HTTP/' in strStatusLine else 0
        
        # Obtém location e content-length 
        strNewHost = next((line[9:].strip() for line in strRespHeader.split('\r\n') 
                            if line.lower().startswith('location:')), None)

        intContentLength = int(next((line[15:].strip() for line in strRespHeader.split('\r\n') 
                                if line.lower().startswith('content-length:')), 0) )
        
        # Salvando o Header da Requisição na porta 80
        strFileName = f'{DIR_APP}\\header_porta_80.txt'
        arqOutput   = open(strFileName, 'w', encoding=CODE_PAGE)
        arqOutput.write(strRespHeader)
        arqOutput.close()

        try:
            # Se o Status Code na classe 3xx, requisita o conteúdo na porta 443 -> SSL
            if 300 <= intStatusCode < 400:
                ...                
                # Porta que Obteve resposta 200
                intPorta = PORT_HTTPS 
        except:
            sys.exit(f'\nERRO.... {sys.exc_info()[0]}\n{sys.exc_info()[1]}')
        else:
            # TODO: Apagar depois
            print(f'\nSocket conectado.................: Porta {intPorta}')
            print(f'Bytes a receber..................: {intContentLength}')

            try:
                # Requisita o Content - GET
                sockTCP.sendall(strReqContent.encode(CODE_PAGE))
            except:
                sys.exit(f'\nERRO.... {sys.exc_info()[0]}\n{sys.exc_info()[1]}')
            else:
                # TODO: Apagar depois
                print('='*50) 
                intPacote = 1

                #boolHeader = False
                #strHeader  = ''
                strContent = ''

                # Obtém o Content da Requisição
                while True:
                    # Recebe os dados do server
                    strDadosRec = sockTCP.recv(BUFFER_SIZE).decode(CODE_PAGE).rstrip()

                    # Interrompe o laço caso não receba nenhum dado
                    if not strDadosRec: break

                    # TODO: Corrigir -> Considerando pacotes não completos                        
                    strContent += strDadosRec
                    
                    # TODO: Apagar depois
                    print(f'Pacote: {intPacote:>4d} - {len(strDadosRec):>4d}') # - {len(strContent):>5d}', flush=True)
                    intPacote += 1

                # TODO: Apagar depois
                print('='*50)

        # Fechando o socket
        sockTCP.close()