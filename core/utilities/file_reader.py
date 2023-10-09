import os

from core import ROOT_PATH_CORE


class FileReader:
    __resource_folder = "resources"

    @staticmethod
    def is_resource_file_exist(file_name: str, root_path: str = ROOT_PATH_CORE):
        return os.path.exists(FileReader.__get_resource_file_path(file_name, root_path))

    @staticmethod
    def get_resource_file(file_name: str, root_path: str = ROOT_PATH_CORE) -> str:
        file_path = FileReader.__get_resource_file_path(file_name, root_path)
        if FileReader.is_resource_file_exist(file_name):
            with open(file_path, "r") as file:
                return file.read()
        raise FileExistsError(f"There are not existing files by path '{file_path}'")

    @staticmethod
    def __get_resource_file_path(file_name: str, root_path: str):
        return os.path.join(root_path, FileReader.__resource_folder, file_name)
