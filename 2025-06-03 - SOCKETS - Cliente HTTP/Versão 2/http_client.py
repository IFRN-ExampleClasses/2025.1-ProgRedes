'''
    Função principal da aplicação
'''
import socket, sys, os

from constantes import *
from lib_funcoes import *

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
