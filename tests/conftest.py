import os
from pathlib import Path

import pytest

from python_selenium_core.logging.logger import Logger
from python_selenium_core.utilities.root_path_helper import RootPathHelper


@pytest.fixture(scope="session", autouse=True)
def setup_session(request):
    # TODO: workaround to set calling root path, because pytest runs from the root dir
    calling_root_path = RootPathHelper.current_root_path(str(Path(__file__).parent))
    Logger.info(f"Setting calling_root_path: {calling_root_path}")
    os.environ["calling_root_path"] = calling_root_path
    yield
