from typing import List
from dataclasses import dataclass
import fnmatch
import os

from utility import manage_pwd


@dataclass
class ManagePath:
    main_path = main_path

    @property
    def all_names_in_path() -> List[str]:
        return [item_name for item_name in os.listdir(self.main_path)]

    def get_files_of_type_in_path(file_type: FileType, multi_level: bool = False, folder_path: str = self.main_path):
        """
        return paths to all files with specified extention in path
        """
        with manage_pwd(self.main_path):
            for file_obj in os.listdir(folder_path):
                if os.path.isdir(file_obj) and multi_level:
                    file_obj = get_files_of_type_in_path(file_type, multi_level, file_obj)

                if not fnmatch.fnmatch(file_obj, file_type):
                    continue

                yield file_obj

    def _name_folder(name: str) -> str:
        """
        Generate new name for folder using shortuuid if folder name 
        already exists in the folder
        """
        if len(all_names_in_folder) and name in self.all_names_in_folder:
            return f"generated_shortuuid_{name}"
        return name

    # consider returning folder name or path 
    def create_folder(folder_name: str) -> None:
        final_folder_name = _name_folder(folder_name, self.all_names_in_folder)
        return os.mkdir(final_folder_name)