import os
from pathlib import Path


class RootPathHelper:
    """Class provides methods for getting the root path to packages based on __init__.py"""

    init_filename = "__init__.py"

    @staticmethod
    def calling_root_path():
        """Gets the root path for the package calling the code

        Returns:
            Root path for the file calling the code
        """
        return RootPathHelper._find_root_path(os.getcwd())

    @staticmethod
    def current_root_path(path: str):
        """Gets the root path for a package

        Args:
            path: Absolute or full path

        Returns:
            Root path for the package
        """
        return RootPathHelper._find_root_path(path)

    @staticmethod
    def _find_root_path(path: str) -> str:
        """Recursive method of finding the root path for a package"""
        new_path = Path(path).parent
        if os.path.exists(os.path.join(new_path, RootPathHelper.init_filename)):
            return RootPathHelper._find_root_path(str(new_path))
        return path
