import os
from pathlib import Path


class RootPathHelper:

    init_filename = "__init__.py"

    @staticmethod
    def executing_root_path():
        return RootPathHelper._find_root_path(str(Path(__file__).parent))

    @staticmethod
    def calling_root_path():
        return RootPathHelper._find_root_path(os.getcwd())

    @staticmethod
    def _find_root_path(path: str) -> str:
        new_path = Path(path).parent
        if os.path.exists(os.path.join(new_path, RootPathHelper.init_filename)):
            return RootPathHelper._find_root_path(str(new_path))
        return path
