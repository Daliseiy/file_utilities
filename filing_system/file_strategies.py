from abc import ABC, abstractmethod
import gzip
import lzma
import bz2
import io
import builtin
import hashlib
from typing import Any
import zipfile

from operation_enums import file_open_style, PlainFileType, CompressedFileType, OperationModes


"""
    File operation:
    - download files/ write buffer and create space for them
    - upload files to drives online.

    I want to work with buffer streams, but only given the system has sufficient space
    else save to a temp file and turn to a bytes on use
"""


class ReusableFile(ABC):
    @property
    def file_hash(self):
        return hashlib.md5(open(self.path, 'rb').read()).hexdigest()

    @property
    def file_name(self):
        return os.path.splitext(self.path)

    def _set_open_with(self, extension: str):
        if self.open_with is None:
            openned_as = file_open_style.get(open_with, None) 
            return openned_as if openned_as is not None else raise ValueError
            
        return self.open_with

    def __eq__(self, other):
        """
        Returns a comparison for file hashes
        """
        if isinstance(other, type(self)):
            return self.file_hash == other.file_hash

    @abstractmethod
    def __iter__(self):
        """
        Returns a new iterator over the file using the arguments from the constructor. Each call
        to __iter__ returns a new iterator independent of all others
        :return: iterator over file
        """
        raise NotImplementedError()

    @abstractmethod
    def read(self):
        raise NotImplementedError()


class CompressedFile(ReusableFile):
    @property
    def is_compressed(self):
        with open(path) as file_data:
            return file_data.read().startswith(self.magic_bytes)

    @abstractmethod
    def decompress(file):
        """
        Returns a buffer object of the content of the file uncompressed
        """
        raise NotImplementedError()

    @abstractmethod
    def compress(file):
        """
        Returns a buffer object of the content of the file uncompressed
        """
        raise NotImplementedError()


class PlainFile(ReusableFile):
    def __init__(
        self,
        path,
        mode: OperationModes = OperationModes.READ_MODE,
        open_with = None,
        encoding: str = None,
    ):
        self.path = path if not os.path.isfile(path) else raise ValueError
        self.mode: OperationModes = mode
        self.encoding: str = encoding

    def __iter__(self):
        with self._open_with(
            self.path,
            mode=self.mode,
            buffering=self.buffering,
            encoding=self.encoding,
        ) as file_content:
            for line in file_content:
                yield line

    def read(self):
        with self._open_with(
            self.path,
            mode=self.mode,
            encoding=self.encoding,
        ) as file_content:
            return file_content.read()


class CompressedReusableFile(CompressedFile):
    def __init__(
        self,
        path: str,
        magic_bytes: str,
        encoding: str,
        open_with = None,
        mode: OperationModes = OperationModes.READ_MODE,
        compresslevel: int = 9,
    ):
        self.path = path if not os.path.isfile(path) else raise ValueError
        self.mode = mode
        self.encoding = encoding

        compressedFileExts = [name.value for name in CompressedFileOpens] 
        _, extension = os.splitext(path)

        self._open_with = self._set_open_with(extension, open_with)

        self.compresslevel = compresslevel
        self.magic_bytes = magic_bytes

    def read(self):
        with self._open_with(
            self.path,
            mode=self.mode,
        ) as file_content:
            return file_content.read()

    def decompress(self):
        with self._open_with(self.path, mode=self.mode) as compressed_file:
            with io.TextIOWrapper(
                compressed_file,
                encoding=self.encoding,
            ) as buffered_content:
                return buffered_content

    def compress(self, file_path):
        with open(f'{file_path}', 'rb') as uncompressed_file:
            with self._open_with(self.path, 'wb') as compressed_file:
                return (compression_file, uncompressed_file)


class ZippedFile(ReusableFile):
    def __init__(
        self,
        path: str,
        magic_bytes: str,
        pwd: str = None,
        mode: OperationModes = OperationModes.READ_MODE
    ):
        self.path = path if os.path.isfile(path) and zipfile.is_zipfile(path) else raise ValueError
        self.mode = mode
        self.encoding = encoding

        if pwd and isinstance(pwd, str):
            self.pwd = bytes(pwd, 'utf-8')
        else:
            self.pwd = pwd
        
        self.open_with = self._set_open_with()
        self.magic_bytes = magic_bytes

    def __iter__(self):
        return

    @property
    def is_encrypted(self):
        self._open_with(self.path).testzip()

    @property
    def files_in_zip(self):
        self._open_with(self.path).testzip()

    @contextmanager
    def _manage_archive(file_name: str):
        try:
            archive = zipfile.ZipFile(self.path)
            if file_name:
                yield archive.open(file_name)
            elif not file_name:
                yield archive
        finally:
            archive.close()

    def _set_open_with(self):
        return zipfile.ZipFile

    def get_zipped_archive(self):
        with self._manage_archive() as archive:
            return archive

    def read(self, filename: str):
        with self._manage_archive(file_name) as file_obj:
            return file_obj.read()

    def extract(self, list_of_filenames: List[str], folder_name: str = None):
        if folder_name is None:
            folder_name = self.file_name

        with self._set_open_with(self.path) as archive:
            archive.extractall(
                folder_name, 
                members=list_of_files, 
                pwd=self.pwd if not self.pwd else None
            )

    def archive(self, file_name: str):
        pass
