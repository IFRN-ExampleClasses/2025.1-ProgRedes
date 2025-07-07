import socket, os

from constantes import *

# ------------------------------------------------------------
def getAjuda():
   strAjuda  = '\nAJUDA DO APP:\n'
   strAjuda += '\? -> Ajuda\n'
   strAjuda += '\\f -> Lista os Arquivos do Servidor\n'
   strAjuda += '\\d:nome_arquivio -> Copia o arquivo para o Cliente\n'
   return strAjuda


# ------------------------------------------------------------
def enviarArquivo(sockDestino: socket, strNomeArquivo: str, destino: tuple[str, int]) -> bool:
   try:
      # Verifica se o arquivo existe e tem permissão de leitura
      if not os.path.isfile(strNomeArquivo):
         raise FileNotFoundError(f'ERRO: Arquivo \'{strNomeArquivo}\' não encontrado.')

      if not os.access(strNomeArquivo, os.R_OK):
         raise PermissionError(f'ERRO: Sem permissão para ler o arquivo \'{strNomeArquivo}\'.')

      # Obtém metadados
      intTamanhoArquivo = os.path.getsize(strNomeArquivo)
      strNomeBase       = os.path.basename(strNomeArquivo)

      # Envia metadados: nome do arquivo e tamanho
      try:
         strCabecalho = f'{strNomeBase}|{intTamanhoArquivo}'
         sockDestino.sendto(strCabecalho.encode(), destino)
      except socket.gaierror as e:
         raise socket.gaierror(f'ERRO: Erro de endereço/host: {e}')
      except socket.timeout as e:
         raise socket.timeout(f'ERRO: Tempo esgotado ao enviar cabeçalho: {e}')
      except socket.error as e:
         raise socket.error(f'ERRO: Erro de socket ao enviar cabeçalho: {e}')

      # Envia o conteúdo do arquivo em blocos
      try:
         arqArquivoEnvio = open(strNomeArquivo, 'rb')
         while True:
            bytesEnvio = arqArquivoEnvio.read(BUFFER_SIZE)
            if not bytesEnvio: break
            sockDestino.sendto(bytesEnvio, destino)
         arqArquivoEnvio.close()
      except Exception as e:
         raise Exception(f'ERRO: Erro ao enviar dados do arquivo: {e}')

      return True

   except Exception as e:
      raise e