def extrairDados(url: str) -> tuple:
    # Encontrar o índice do '://' - Ignorando "https://"
    intInicioHost = url.find('://') + 3
    
    # Encontrar o índice do primeiro '/' após '://'
    intFinalHost = url.find('/', intInicioHost)
    
    # Extrair o host
    hostURL = url[intInicioHost:intFinalHost]
    
    # Extrair o caminho sem o nome do arquivo (tudo após o host, menos o arquivo)
    hostPath = url[intFinalHost:]
    
    # O nome da imagem é a última parte do caminho
    hostNomeImagem = hostPath.split('/')[-1]

    # Remover o nome do arquivo do caminho (parte após o último '/')
    hostPath = '/'.join(hostPath.split('/')[:-1])
    
    
    return hostURL, hostPath, hostNomeImagem


# ------------------------------------------------------------------------------------------
# URL de exemplo
strURL = 'https://www.coralplaza.com.br/wp-content/uploads/2018/09/203768-5-motivos-para-voce-conhecer-a-praia-de-ponta-negra-1.jpg'

# Chamada da função
strHost, strCaminho, strNomeImagem = extrairDados(strURL)

# Exibindo os resultados
print(f'Host..........: {strHost}')
print(f'Nome da Imagem: {strNomeImagem}')
print(f'Caminho.......: {strCaminho}')
