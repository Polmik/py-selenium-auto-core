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
        return os.path.exists(FileReader.get_resource_file_path(file_name, root_path))

    @staticmethod
    def get_resource_file(file_name: str, root_path: Optional[str] = None) -> str:
        """Gets information from the file in the Resources folder

        Args:
            file_name: Name of resource file
            root_path: Root path which resource belongs to

        Returns:
            Text of the file

        'get_resource_file' is deprecated. Use 'property' with 'abstractmethod' instead.
        """
        file_path = FileReader.get_resource_file_path(file_name, root_path)
        if FileReader.is_resource_file_exist(file_name, root_path):
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        message = f"""There are not existing files by path '{file_path}'
        
        Perhaps the tests were run from the root directory, which caused difficulties in finding the necessary files. 
            To solve the problem, try adding work_dir from the test package to the setup_session fixture
        
        @pytest.fixture(scope="session", autouse=True)
        def setup_session(request):
            work_dir = RootPathHelper.current_root_path(__file__)
            os.chdir(work_dir)
        """
        raise FileExistsError(message)

    @staticmethod
    def get_resource_file_path(file_name: str, root_path: str) -> str:
        root_path = root_path or RootPathHelper.current_root_path(__file__)
        return os.path.join(root_path, FileReader.__resource_folder, file_name)
