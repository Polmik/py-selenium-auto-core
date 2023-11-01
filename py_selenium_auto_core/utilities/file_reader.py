import os
from typing import Optional

from py_selenium_auto_core.utilities.root_path_helper import RootPathHelper


class FileReader:
    """Utility methods to read files"""

    __resource_folder = "resources"

    @staticmethod
    def is_resource_file_exist(file_name: str, root_path: Optional[str] = None) -> bool:
        """Checks whether file exists in Resources folder or not

        Args:
            file_name: Name of resource file
            root_path: Root path which resource belongs to

        Returns:
            True if exists and false otherwise
        """
        return os.path.exists(FileReader.__get_resource_file_path(file_name, root_path))

    @staticmethod
    def get_resource_file(file_name: str, root_path: Optional[str] = None) -> str:
        """Gets information from the file in the Resources folder

        Args:
            file_name: Name of resource file
            root_path: Root path which resource belongs to

        Returns:
            Text of the file
        """
        file_path = FileReader.__get_resource_file_path(file_name, root_path)
        if FileReader.is_resource_file_exist(file_name, root_path):
            with open(file_path, "r", encoding='utf-8') as file:
                return file.read()
        raise FileExistsError(f"There are not existing files by path '{file_path}'")

    @staticmethod
    def __get_resource_file_path(file_name: str, root_path: str) -> str:
        root_path = root_path or RootPathHelper.executing_root_path()
        return os.path.join(root_path, FileReader.__resource_folder, file_name)
