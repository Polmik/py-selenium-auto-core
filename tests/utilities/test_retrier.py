import time
from typing import Callable

from python_selenium_core.applications.startup import Startup
from python_selenium_core.configurations.retry_configuration import RetryConfiguration
from python_selenium_core.logging.logger import Logger
from tests.applications.browser.browser_service import BrowserService


class TestRetrier:

    accuracy: int = 100

    @property
    def logger(self) -> Logger:
        return BrowserService.service_provider().logger()

    @property
    def retry_configuration(self) -> RetryConfiguration:
        return BrowserService.service_provider().retry_configuration()

    @property
    def polling_interval(self) -> float:
        return self.retry_configuration.polling_interval * 1000

    def setup_method(self, method):
        Startup.configure_services(lambda: BrowserService.application())

    def retrier_should_work_once(self, function: Callable):
        start_time = time.time()
        function()
        duration = time.time() - start_time
        assert duration < self.polling_interval, \
            f"Duration '{duration}' should be less that pollingInterval '{self.polling_interval}'"

    def retrier_should_wait_polling_interval(self, function: Callable):
        start_time = time.time()
        function()
        duration = (time.time() - start_time) * 1000
        doubled_accuracy_polling_interval = self.polling_interval * 2 + self.accuracy
        assert self.polling_interval <= duration <= doubled_accuracy_polling_interval, \
            f"Duration '{duration}' should be more than '{self.polling_interval}' " \
            f"and less than '{doubled_accuracy_polling_interval}'"

    def retrier_should_work_correct_times(self, exception, actual_attempts, function: Callable):
        try:
            function()
        except Exception as ex:
            assert isinstance(ex, exception)
        assert actual_attempts[0] == self.retry_configuration.number + 1, \
            "actual attempts count is not match to expected"
