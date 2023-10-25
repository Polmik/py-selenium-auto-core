import os
from typing import Optional

from python_selenium_core.utilities.root_path_helper import RootPathHelper


class FileReader:
    __resource_folder = "resources"

    @staticmethod
    def is_resource_file_exist(file_name: str, root_path: Optional[str] = None) -> bool:
        return os.path.exists(FileReader.__get_resource_file_path(file_name, root_path))

    @staticmethod
    def get_resource_file(file_name: str, root_path: Optional[str] = None) -> str:
        file_path = FileReader.__get_resource_file_path(file_name, root_path)
        if FileReader.is_resource_file_exist(file_name, root_path):
            with open(file_path, "r", encoding='utf-8') as file:
                return file.read()
        raise FileExistsError(f"There are not existing files by path '{file_path}'")

    @staticmethod
    def __get_resource_file_path(file_name: str, root_path: str) -> str:
        root_path = root_path or RootPathHelper.executing_root_path()
        return os.path.join(root_path, FileReader.__resource_folder, file_name)
