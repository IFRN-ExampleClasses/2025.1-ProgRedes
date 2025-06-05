'''
   Este exemplo solicita um HOST ou uma URL e obtem o cabeçalho 
   e o conteúdo da resposta da requisição seguindo o padrão do 
   protocolo HTTP
'''
import socket, sys, os, ssl

# --------------------------------------------------
# Constantes do Programa
PORT_HTTP = 80
PORT_HTTPS = 443
CODE_PAGE = 'utf-8'
BUFFER_SIZE = 4096

# Templates de requisição
REQ_HEAD_TEMPLATE = 'HEAD / HTTP/1.1\r\nHost: {}\r\nAccept: text/html\r\nConnection: close\r\n\r\n'
REQ_GET_TEMPLATE  = 'GET / HTTP/1.1\r\nHost: {}\r\nAccept: text/html\r\nConnection: close\r\n\r\n'

# Diretório da Aplicação
DIR_APP = os.path.dirname(__file__)
# --------------------------------------------------


# --------------------------------------------------
# Obtém o Status Code da Requisição
def obterStatusCode(headerResposta: str) -> int:
    strStatusLine = headerResposta.split('\r\n')[0]
    intStatusCode = int(strStatusLine.split(' ')[1]) if 'HTTP/' in strStatusLine else 0
    return intStatusCode

# --------------------------------------------------
# Extrai informações do HEADER
def extrairHeaders(headerResposta: str) -> tuple:
    strNovoHost = next((line[9:].strip() for line in headerResposta.split('\r\n') 
                      if line.lower().startswith('location:')), None)
    
    intTamanhoConteudo = int(next((line[15:].strip() for line in headerResposta.split('\r\n') 
                                 if line.lower().startswith('content-length:')), 0))
    
    return (strNovoHost, intTamanhoConteudo)

# --------------------------------------------------
# Cria um SOCKET SSL
def criarSocketSSL(host: str) -> socket:
    context = ssl.create_default_context()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = context.wrap_socket(sock, server_hostname=host)
    return ssl_sock

# --------------------------------------------------
# Recebe a resposta HTTP completa
def obterFullResponse(sock: socket) -> str:
    data = b''
    while True:
        part = sock.recv(BUFFER_SIZE)
        if not part: break
        data += part
    return data.decode(CODE_PAGE, errors='ignore')

# --------------------------------------------------
# Cria um diretório com o nome do host se não existir
def criarDiretorioHost(host: str) -> str:
    host_clean = host.replace('http://', '').replace('https://', '').split('/')[0]
    host_clean = host_clean.split(':')[0]
    
    dir_host = os.path.join(DIR_APP, host_clean)
    if not os.path.exists(dir_host):
        os.makedirs(dir_host)
    return dir_host

# --------------------------------------------------
def main():
    # Solicitando o host ao usuário
    strHost = input('\nInforme o nome do HOST ou URL do site: ').strip()

    # Remove HTTP:// ou HTTPS://
    strHost = strHost.replace('http://', '').replace('https://', '').split('/')[0]

    # Cria diretório para o host
    dir_host = criarDiretorioHost(strHost)

    try:
        # Primeiro tentamos HTTP na porta 80
        sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sockTCP.settimeout(10)
        sockTCP.connect((strHost, PORT_HTTP))
        
        # Requisita o Header
        sockTCP.sendall(REQ_HEAD_TEMPLATE.format(strHost).encode(CODE_PAGE))
        strRespHeader = obterFullResponse(sockTCP)
        sockTCP.close()
        
        # Obtém informações do cabeçalho
        intStatusCode = obterStatusCode(strRespHeader)
        strNewHost, _ = extrairHeaders(strRespHeader)
        
        # Salvando o Header da Requisição na porta 80
        with open(os.path.join(dir_host, 'header_porta_80.txt'), 'w', encoding=CODE_PAGE) as f:
            f.write(strRespHeader)
        
        # Se houver redirecionamento para HTTPS
        if 300 <= intStatusCode < 400 and strNewHost:
            new_host = strNewHost.split('//')[-1].split('/')[0]
            
            # Cria novo socket SSL
            sockTCP = criarSocketSSL(new_host)
            #sockTCP.settimeout(10)
            sockTCP.connect((new_host, PORT_HTTPS))
            
            # Envia requisição GET para obter conteúdo completo
            sockTCP.sendall(REQ_GET_TEMPLATE.format(new_host).encode(CODE_PAGE))
            full_response = obterFullResponse(sockTCP)
            
            # Separa headers do conteúdo
            if '\r\n\r\n' in full_response:
                strRespHeaders, strContent = full_response.split('\r\n\r\n', 1)
            else:
                strRespHeaders, strContent = full_response, ''
            
            # Salvando o Header da nova porta
            with open(os.path.join(dir_host, f'header_porta_{PORT_HTTPS}.txt'), 'w', encoding=CODE_PAGE) as f:
                f.write(strRespHeaders)
            
            # Exibe informações
            print(f'\nRedirecionado para............: {new_host}')
            print(f'Socket conectado..............: Porta {PORT_HTTPS}')
            print(f'Tamanho do conteúdo...........: {len(strContent)} bytes')
            
            # Salva o conteúdo
            with open(os.path.join(dir_host, f'conteudo_porta_{PORT_HTTPS}.txt'), 'w', encoding=CODE_PAGE) as f:
                f.write(strContent)
        else:
            # Se não houve redirecionamento, faz GET na porta 80
            sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #sockTCP.settimeout(10)
            sockTCP.connect((strHost, PORT_HTTP))
            sockTCP.sendall(REQ_GET_TEMPLATE.format(strHost).encode(CODE_PAGE))
            full_response = obterFullResponse(sockTCP)
            
            if '\r\n\r\n' in full_response:
                strRespHeaders, strContent = full_response.split('\r\n\r\n', 1)
            else:
                strRespHeaders, strContent = full_response, ''
            
            print(f'\nSocket conectado..............: Porta {PORT_HTTP}')
            print(f'Tamanho do conteúdo..........: {len(strContent)} bytes')
            
            with open(os.path.join(dir_host, f'conteudo_porta_{PORT_HTTP}.txt'), 'w', encoding=CODE_PAGE) as f:
                f.write(strContent)
                
    except Exception as e:
        sys.exit(f'\nERRO.... {type(e).__name__}\n{str(e)}')
    finally:
        if 'sockTCP' in locals(): 
            sockTCP.close()

if __name__ == '__main__': 
    main()