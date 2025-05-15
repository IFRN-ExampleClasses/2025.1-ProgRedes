# ------------------------------------------------------------------------------------------
# Esta versão exibe os dados brutos (RAW) extraídos do HEADER do arquivo
# e os dados tratados, exibindo assim os valores obtidos de cada metadado 
# ------------------------------------------------------------------------------------------

import sys
from metadata_constantes import *

strNomeArq = DIR_IMG + '\\presepio_natalino.jpg'

try:
   fileContent = open(strNomeArq, 'rb')
except FileNotFoundError:
   sys.exit('\nERRO: Arquivo Não Existe...\n')
except:
   sys.exit(f'\nERRO: {sys.exc_info()[1]}...\n')
else:
   # Verificando se o arquivo informado é JPG 
   if fileContent.read(2) != b'\xFF\xD8':
      fileContent.close()
      sys.exit('\nERRO: Arquivo informado não é JPG...\n')

   # Verifica se o arquivo possui metadados
   if fileContent.read(2) != b'\xFF\xE1':
      fileContent.close()
      sys.exit('\nAVISO: Este arquivo não possui metadados...\n')

   # ------------------------------------------------------------------------
   # Obtendo EXIF
   exifSize      = fileContent.read(2)
   exifHeader    = fileContent.read(4) # EXIF Header (marcador EXIF)
   temp1         = fileContent.read(2) # EXIF Header (fixo)
   tiffHeader    = fileContent.read(2) # (49 49: Little Endian - Intel / 4D 4D: Big Endian - Motorola)
   temp2         = fileContent.read(2) # TIFF Header (fixo)
   temp3         = fileContent.read(4) # TIFF Header (fixo)
   countMetadata = fileContent.read(2) # Metadata Count

   exifSize      = int.from_bytes(exifSize, byteorder=BYTE_ORDER[tiffHeader])
   countMetadata = int.from_bytes(countMetadata, byteorder=BYTE_ORDER[tiffHeader])

   dictEXIF = { 'exifSize' : exifSize, 'exifMarker': exifHeader, 
                'temp1'    : temp1   , 'tiffHeader': tiffHeader, 
                'temp2'    : temp2   , 'temp3'     : temp3,
                'metaCount': countMetadata}

   # Imprimindo os resultados
   print('\n\nINÍCIO DO HEADER')
   print('-'*80)
   print(f'{dictEXIF}\n\n')

   # ------------------------------------------------------------------------
   # Obtendo os Metadados Brutos
   lstRAWMetaData = list()
   boolGPSInfo    = False
   for _ in range(countMetadata):
      idTAGNumber      = fileContent.read(2) # Identificador do Metadado
      idDataFormat     = fileContent.read(2)  # Tipo do Metadado
      numberComponents = fileContent.read(4) # Qt. Repetições do Metadado
      dataValue        = fileContent.read(4) # Valor do Metadado / Se maior que 4 bytes -> indica Offset
      
		# Adicionando os Metadados lidos a  lista de metadados brutos
      lstTemp = [idTAGNumber, idDataFormat, numberComponents, dataValue]
      lstRAWMetaData.append(dict(zip(METADATA_HEADER, lstTemp)))

      # Verifica se existe a tag GPSINFO
      if idTAGNumber == b'\x25\x88':
         # Deslocando o ponteiro de leitura para a posição dos dados do GPS
         intGPSOffSet = int.from_bytes(dataValue, byteorder=BYTE_ORDER[tiffHeader])
         if intGPSOffSet <= 0: continue
         fileContent.seek(intGPSOffSet + 12, 0)

         # Obtendo a quantidade de informações do GPS
         gpsDataCount = fileContent.read(2)
         gpsDataCount = int.from_bytes(gpsDataCount, byteorder=BYTE_ORDER[tiffHeader])

         # Montando a lista com os dados brutos do  GPS
         lstRAWGPSData = list()
         for _ in range(gpsDataCount):
            idTAGNumber      = fileContent.read(2)
            idDataFormat     = fileContent.read(2)
            numberComponents = fileContent.read(4)
            dataValue        = fileContent.read(4)
      
            lstTemp = [idTAGNumber, idDataFormat, numberComponents, dataValue]
            lstRAWGPSData.append(dict(zip(METADATA_HEADER, lstTemp)))         

   # Imprimindo os metadados brutos
   if PRINT_RAW:
      print('METADADOS - LIDOS (BRUTOS)')
      print('-'*80)
      for metaData in lstRAWMetaData: print(metaData)
      print('\n')
      print('METADADOS GPS - LIDOS (BRUTOS)')
      for metaData in lstRAWGPSData: print(metaData)
      print('\n\n')


   # ------------------------------------------------------------------------
   # Invertendo os bytes das chaves dos dicionário 
   # TAG_NUMBER e GPS_TAG_NUMBER (padrão II)
   if tiffHeader == b'\x49\x49':
      TAG_NUMBER     = {key[::-1]: value for key, value in TAG_NUMBER.items()}
      GPS_TAG_NUMBER = {key[::-1]: value for key, value in GPS_TAG_NUMBER.items()}

   # ------------------------------------------------------------------------
   # Tratando os dados brutos obtidos
   lstDEALMetaData = list()
   for data in lstRAWMetaData:
      strTAGName      = TAG_NUMBER[data['TAGNumber']]
      strDataFormat   = DATA_FORMAT[data['DataFormat']]
      intQtCaracteres = int.from_bytes(data['NumberComponents'], byteorder=BYTE_ORDER[tiffHeader])
      valorData       = int.from_bytes(data['DataValue'], byteorder=BYTE_ORDER[tiffHeader])
      if strDataFormat == 'ASCII String':
         fileContent.seek(valorData+12,0)
         valorData = fileContent.read(intQtCaracteres).decode(CODE_PAGE).rstrip('\x00')
      lstTemp = [strTAGName, strDataFormat, intQtCaracteres, valorData]
      lstDEALMetaData.append(dict(zip(METADATA_HEADER, lstTemp)))


   # ------------------------------------------------------------------------
   # Tratando os dados do GPS brutos obtidos
   lstDEALGPSData = list()
   for data in lstRAWGPSData:
      strTAGName      = GPS_TAG_NUMBER.get(data['TAGNumber'], 'Desconhecido')
      strDataFormat   = DATA_FORMAT[data['DataFormat']]
      intQtCaracteres = int.from_bytes(data['NumberComponents'], byteorder=BYTE_ORDER[tiffHeader])
      valorData       = int.from_bytes(data['DataValue'], byteorder=BYTE_ORDER[tiffHeader])      
      
      if strDataFormat == 'ASCII String':
         intPosAtual = fileContent.tell()
         fileContent.seek(valorData + 12 + intGPSOffSet, 0)
         try:
            #valorData = fileContent.read(intQtCaracteres).decode('latin-1').rstrip('\x00')
            valorData = fileContent.read(intQtCaracteres).decode(CODE_PAGE)
            strTAGName += ' (OK)'
         except UnicodeDecodeError:
            valorData = fileContent.read(intQtCaracteres).hex()
            strTAGName += ' (*)'
         fileContent.seek(intPosAtual)
      elif strDataFormat in ['Unsigned Rational', 'Signed Rational']:
         intPosAtual = fileContent.tell()
         fileContent.seek(valorData + 12 + intGPSOffSet, 0)
         intNumerador   = int.from_bytes(fileContent.read(4), byteorder=BYTE_ORDER[tiffHeader])
         intDenominador = int.from_bytes(fileContent.read(4), byteorder=BYTE_ORDER[tiffHeader])
         if intDenominador != 0:
            valorData = intNumerador / intDenominador
         else:
            valorData = 0
         fileContent.seek(intPosAtual)
 
      lstTemp = [strTAGName, strDataFormat, intQtCaracteres, valorData]
      lstDEALGPSData.append(dict(zip(METADATA_HEADER, lstTemp)))

   # ------------------------------------------------------------------------
   # Fechando o arquivo
   fileContent.close()

   # ------------------------------------------------------------------------
   # Imprimindo os metadatas tratados
   if PRINT_DEAL:
      print('METADADOS LIDOS (TRATADOS)')
      print('-'*80)
      for metaData in lstDEALMetaData: print(metaData)

   for metaData in lstDEALGPSData: print(metaData)
