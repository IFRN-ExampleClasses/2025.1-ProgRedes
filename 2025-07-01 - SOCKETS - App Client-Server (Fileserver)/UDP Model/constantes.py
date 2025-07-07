import os

from funcoes_genericas import *

# --------------------------------------------------------------------------------
HOST_IP_SERVER    = getLocalIP()    # Definindo o IP do servidor para os clientes
HOST_PORT         = 40000           # Definindo a porta

CODE_PAGE         = 'utf-8'         # Definindo a página de caracteres
BUFFER_SIZE       = 512             # Tamanho do buffer

DIR_IMG_SERVER    = os.path.dirname(__file__) + '\\server_files\\'
DIR_IMG_CLIENT    = os.path.dirname(__file__) + '\\client_files\\'
# --------------------------------------------------------------------------------