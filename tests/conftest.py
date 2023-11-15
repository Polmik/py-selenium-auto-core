import logging
import os
from pathlib import Path

import pytest

from py_selenium_auto_core.logging.logger import Logger
from py_selenium_auto_core.utilities.root_path_helper import RootPathHelper


@pytest.fixture(scope="session", autouse=True)
def setup_session(request):
    # TODO: workaround to set calling root path, because pytest runs from the root dir
    calling_root_path = RootPathHelper.current_root_path(str(Path(__file__).parent))
    os.environ["calling_root_path"] = calling_root_path
    Logger.info(f"Setting calling_root_path: {calling_root_path}")

    for log_name in [
        "selenium.webdriver.remote.remote_connection",
        "selenium.webdriver.common.selenium_manager",
        "urllib3.connectionpool",
    ]:
        logger = logging.getLogger(log_name)
        logger.disabled = True
    yield
