import socket

from constantes import *

# ------------------------------------------------------------
def getLocalIP():
   # Obtém o nome da máquina (localhost)
   strHostName = socket.gethostname()

   # Obtém o IP local associado ao nome da máquina
   strIPHost = socket.gethostbyname(strHostName)

   return strIPHost
