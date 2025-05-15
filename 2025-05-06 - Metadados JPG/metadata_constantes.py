import os

# --------------------------------------------------------------------------------
# Diretório onde a aplicação está armazenada
DIR_APP = os.path.dirname(__file__)

# Diretório onde as imagens estão armazenadas
DIR_IMG = DIR_APP + '\\images'

# Define a página de códigos de caracteres
CODE_PAGE  = 'utf-8'

# Define se os dados brutos serão impressos
PRINT_RAW  = True    

# Define se os dados tratados serão impressos
PRINT_DEAL = False   


# --------------------------------------------------------------------------------
EXIF_HEADER     = ['exifSize', 'exifMarker', 'temp1', 'tiffHeader', 'temp2', 'temp3', 'metaCount']
METADATA_HEADER = ['TAGNumber', 'DataFormat', 'NumberComponents', 'DataValue']

# (b'\x49\x49': Little Endian - Intel / b'\x4D\xD9': Big Endian - Motorola)
BYTE_ORDER  = { b'\x49\x49': 'little', b'\x4D\x4D': 'big' }

TAG_NUMBER  = { 
   b'\x01\x0e': 'ImageDescription'        , b'\x01\x0f': 'Make',
   b'\x01\x10': 'Model'                   , b'\x01\x12': 'Orientation',
   b'\x01\x1a': 'XResolution'             , b'\x01\x1b': 'YResolution',
   b'\x01\x28': 'ResolutionUnit'          , b'\x01\x31': 'Software',
   b'\x01\x32': 'DateTime'                , b'\x01\x3e': 'WhitePoint',
   b'\x01\x3f': 'PrimaryChromaticitie'    , b'\x02\x11': 'YCbCrCoefficients',
   b'\x02\x13': 'YCbCrPositioning'        , b'\x02\x14': 'ReferenceBlackWhite',
   b'\x82\x98': 'Copyright'               , b'\x87\x69': 'ExifOffset',
   b'\x01\x00': 'ImageWidth'              , b'\x01\x01': 'ImageLength',
   b'\x01\x02': 'BitsPerSample'           , b'\x01\x03': 'Compression',
   b'\x01\x06': 'PhotometricInterpretatio', b'\x01\x11': 'StripOffsets',
   b'\x01\x15': 'SamplesPerPixel'         , b'\x01\x16': 'RowsPerStrip',
   b'\x01\x17': 'StripByteConunts'        , b'\x01\x1a': 'XResolution',
   b'\x01\x1b': 'YResolution'             , b'\x01\x1c': 'PlanarConfiguration',
   b'\x01\x28': 'ResolutionUnit'          , b'\x02\x01': 'JpegIFOffset',
   b'\x02\x02': 'JpegIFByteCount'         , b'\x02\x11': 'YCbCrCoefficients',
   b'\x02\x12': 'YCbCrSubSampling'        , b'\x02\x13': 'YCbCrPositioning',
   b'\x02\x14': 'ReferenceBlackWhite'     , b'\x00\xfe': 'NewSubfileType',          
   b'\x00\xff': 'SubfileType'             , b'\x01\x2d': 'TransferFunction',
   b'\x01\x3b': 'Artist'                  , b'\x01\x3d': 'Predictor',
   b'\x01\x42': 'TileWidth'               , b'\x01\x43': 'TileLength',
   b'\x01\x44': 'TileOffsets'             , b'\x01\x45': 'TileByteCounts',
   b'\x01\x4a': 'SubIFDs'                 , b'\x01\x5b': 'JPEGTables',
   b'\x82\x8d': 'CFARepeatPatternDim'     , b'\x82\x8e': 'CFAPattern',
   b'\x82\x8f': 'BatteryLevel'            , b'\x83\xbb': 'IPTC/NAA',
   b'\x87\x73': 'InterColorProfile'       , b'\x88\x24': 'SpectralSensitivity',
   b'\x88\x25': 'GPSInfo'                 , b'\x88\x28': 'OECF',
   b'\x88\x29': 'Interlace'               , b'\x88\x2a': 'TimeZoneOffset',
   b'\x88\x2b': 'SelfTimerMode'           , b'\x92\x0b': 'FlashEnergy',
   b'\x92\x0c': 'SpatialFrequencyResponse', b'\x92\x0d': 'Noise',
   b'\x92\x11': 'ImageNumber'             , b'\x92\x12': 'SecurityClassification',
   b'\x92\x13': 'ImageHistory'            , b'\x92\x14': 'SubjectLocation',
   b'\x92\x15': 'ExposureIndex'           , b'\x92\x16': 'TIFF/EPStandardID',
   b'\x92\x90': 'SubSecTime'              , b'\x92\x91': 'SubSecTimeOriginal',
   b'\x92\x92': 'SubSecTimeDigitized'     , b'\xa2\x0b': 'FlashEnergy',
   b'\xa2\x0c': 'SpatialFrequencyResponse', b'\xa2\x14': 'SubjectLocation',
   b'\xa2\x15': 'ExposureIndex'           , b'\xa3\x02': 'CFAPattern'
}

DATA_FORMAT = {
   b'\x01\x00': 'Unsigned Byte'    , b'\x02\x00': 'ASCII String', 
   b'\x03\x00': 'Unsigned Short'   , b'\x04\x00': 'Unsigned Long', 
   b'\x05\x00': 'Unsigned Rational', b'\x06\x00': 'Signed Byte', 
   b'\x07\x00': 'Undefinied'       , b'\x08\x00': 'Signed Short', 
   b'\x09\x00': 'Signed Long'      , b'\x10\x00': 'Signed Rational', 
   b'\x11\x00': 'Single Float'     , b'\x12\x00': 'Double Float'
}

GPS_TAG_NUMBER = {
   b'\x00\x00': 'GPSVersionID'      , b'\x00\x01': 'GPSLatitudeRef',
   b'\x00\x02': 'GPSLatitude'       , b'\x00\x03': 'GPSLongitudeRef',
   b'\x00\x04': 'GPSLongitude'      , b'\x00\x05': 'GPSAltitudeRef',
   b'\x00\x06': 'GPSAltitude'       , b'\x00\x07': 'GPSTimeStamp',
   b'\x00\x08': 'GPSSatellites'     , b'\x00\x09': 'GPSStatus',
   b'\x00\x0a': 'GPSMeasureMode'    , b'\x00\x0b': 'GPSDOP',
   b'\x00\x0c': 'GPSSpeedRef'       , b'\x00\x0d': 'GPSSpeed',
   b'\x00\x0e': 'GPSTrackRef'       , b'\x00\x0f': 'GPSTrack',
   b'\x00\x10': 'GPSImgDirectionRef', b'\x00\x11': 'GPSImgDirection',
   b'\x00\x12': 'GPSMapDatum'       , b'\x00\x13': 'GPSDestLatitudeRef',
   b'\x00\x14': 'GPSDestLatitude'   , b'\x00\x15': 'GPSDestLongitudeRef',
   b'\x00\x16': 'GPSDestLongitude'  , b'\x00\x17': 'GPSDestBearingRef',
   b'\x00\x18': 'GPSDestBearing'    , b'\x00\x19': 'GPSDestDistanceRef',
   b'\x00\x1a': 'GPSDestDistance'   , b'\x00\x1b': 'GPSProcessingMethod',
   b'\x00\x1c': 'GPSAreaInformation', b'\x00\x1d': 'GPSDateStamp',
   b'\x00\x1e': 'GPSDifferential'
}