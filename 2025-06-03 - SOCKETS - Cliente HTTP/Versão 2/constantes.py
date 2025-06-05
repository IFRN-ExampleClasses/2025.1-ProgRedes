'''
   Arquivo contendo as constantes que serão usadas na aplicação
'''
import os

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