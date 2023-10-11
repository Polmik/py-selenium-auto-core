import os

from python_selenium_core.logging.logger import Logger
from tests.test_without_application import TestWithoutApplication



class TestLocalizationManager(TestWithoutApplication):

    def test1(self):
        Logger.info(os.environ)
        Logger.info(os.environ.get("profile"))
        os.environ['profile'] = "1"
        Logger.info(os.environ.get("profile"))
