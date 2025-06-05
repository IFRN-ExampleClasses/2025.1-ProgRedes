'''
    Biblioteca de funções a serem usadas pela aplicação
'''
import socket, ssl

from constantes import *

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