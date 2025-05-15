# ------------------------------------------------------------------------------------------
# Esta versão exibe apenas os dados brutos (RAW) extraídos do HEADER do arquivo 
# ------------------------------------------------------------------------------------------

import os, sys

# ------------------------------------------------------------------------------------------
DIR_APP = os.path.dirname(__file__)
DIR_IMG = DIR_APP + '\\images'

# ------------------------------------------------------------------------------------------

strNomeArq = DIR_IMG + '\\presepio_natalino.jpg'

try:
    fileInput = open(strNomeArq, 'rb')
except FileNotFoundError:
    sys.exit('\nERRO: Arquivo Não Existe...\n')
except:
    sys.exit(f'\nERRO: {sys.exc_info()[1]}...\n')
else:
    # Verificando se o arquivo informado é JPG 
    if fileInput.read(2) != b'\xFF\xD8':
        fileInput.close()
        sys.exit('\nERRO: Arquivo informado não é JPG...\n')

    # Verifica se o arquivo possui metadados
    if fileInput.read(2) != b'\xFF\xE1':
        fileInput.close()
        sys.exit('\nAVISO: Este arquivo não possui metadados...\n')

    # Obtendo EXIF
    exifSize      = fileInput.read(2)
    exifHeader    = fileInput.read(4) # EXIF Header (marcador EXIF)
    temp1         = fileInput.read(2) # EXIF Header (fixo)
    tiffHeader    = fileInput.read(2) # (49 49: Little Endian - Intel / 4D 4D: Big Endian - Motorola)
    temp2         = fileInput.read(2) # TIFF Header (fixo)
    temp3         = fileInput.read(4) # TIFF Header (fixo)
    countMetadata = fileInput.read(2) # Metadata Count

    if tiffHeader == b'\x49\x49':
        exifSize      = int.from_bytes(exifSize, byteorder='little')
        countMetadata = int.from_bytes(countMetadata, byteorder='little')
    else:
        exifSize      = int.from_bytes(exifSize, byteorder='big')
        countMetadata = int.from_bytes(countMetadata, byteorder='big')

    dictEXIF = { 'exifSize' : exifSize, 'exifMarker': exifHeader, 
                 'temp1'    : temp1   , 'tiffHeader': tiffHeader, 
                 'temp2'    : temp2   , 'temp3'     : temp3,
                 'metaCount': countMetadata}

    # Obtendo os Metadados
    lstMetadata   = list()
    lstMetaHeader = ['TAGNumber', 'DataFormat', 'NumberComponents', 'DataValue']
    for _ in range(countMetadata):
        idTAGNumber      = fileInput.read(2) # Identificador do Metadado
        idDataFormat     = fileInput.read(2) # Tipo do Metadado
        numberComponents = fileInput.read(4) # Qt. Repetições do Metadado
        dataValue        = fileInput.read(4) # Valor do Metadado / Se maior que 4 bytes -> indica Offset
        lstTemp = [idTAGNumber, idDataFormat, numberComponents, dataValue]
        lstMetadata.append(dict(zip(lstMetaHeader, lstTemp)))

    # Fechando o arquivo
    fileInput.close()

    # Imprimindo os resultados
    print('\n\n', dictEXIF, '\n\n')
    
    # Imprimindo os metadatas lidos
    for metaData in lstMetadata: print(metaData)
    print('\n\n')

