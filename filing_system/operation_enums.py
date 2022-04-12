from enum import Enum

class OperationModes(Enum):
    READ_MODE = 'r'
    READ_WRITE_MODE = 'r+'
    WRITE_MODE = 'w' 
    APPEND_MODE = 'a'
    CREATE_MODE = 'x'
    READ_BINARY_MODE = 'rb'
    WRITE_BINARY_MODE = 'wb'
    APPEND_BINARY_MODE = 'r+b'


class CompressedFileType(Enum):
    # ZIP = '.zip'
    GZIP = '.gz'
    BZ2 = '.bz2'
    # TAR = '.tar'


class PlainFileType(Enum):
    TEXT = '.txt'

file_open_style = {
    # CompressedFileType.ZIP: zipfile.ZipFile,
    CompressedFileType.GZIP: gzip.open,
    CompressedFileType.BZ2: bz2.BZ2File,
    # CompressedFileType.TAR: gzip.open
    PlainFileType.TEXT: builtin.open
}