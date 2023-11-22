from typing import Callable

from py_selenium_auto_core.applications.startup import Startup
from py_selenium_auto_core.configurations.retry_configuration import RetryConfiguration
from py_selenium_auto_core.logging.logger import Logger
from py_selenium_auto_core.utilities.functional import Timer
from tests.applications.browser.browser_services import BrowserServices


class TestRetrier:
    accuracy: int = 100

    @property
    def logger(self) -> Logger:
        return BrowserServices.Instance.service_provider.logger()

    @property
    def retry_configuration(self) -> RetryConfiguration:
        return BrowserServices.Instance.service_provider.retry_configuration()

    @property
    def polling_interval(self) -> float:
        return self.retry_configuration.polling_interval

    def setup_method(self):
        Startup.configure_services(lambda: BrowserServices.Instance.application)

    def retrier_should_work_once(self, function: Callable):
        with Timer() as timer:
            function()
        duration = timer.elapsed.total_seconds()
        assert (
            duration < self.polling_interval
        ), f"Duration '{duration}' should be less that pollingInterval '{self.polling_interval}'"

    def retrier_should_wait_polling_interval(self, function: Callable):
        with Timer() as timer:
            function()
        duration = timer.elapsed.total_seconds()
        doubled_accuracy_polling_interval = self.polling_interval * 2 + self.accuracy
        assert self.polling_interval <= duration <= doubled_accuracy_polling_interval, (
            f"Duration '{duration}' should be more than '{self.polling_interval}' "
            f"and less than '{doubled_accuracy_polling_interval}'"
        )

    def retrier_should_work_correct_times(self, exception, actual_attempts, function: Callable):
        try:
            function()
        except Exception as ex:
            assert isinstance(ex, exception)
        assert (
            actual_attempts[0] == self.retry_configuration.number + 1
        ), "actual attempts count is not match to expected"
