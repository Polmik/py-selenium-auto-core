import pytest
from selenium.common import InvalidElementStateException, StaleElementReferenceException

from py_selenium_auto_core.utilities.element_action_retrier import ElementActionRetrier
from tests.applications.browser.browser_service import BrowserService
from tests.utilities.test_retrier import TestRetrier


class TestElementActionRetrier(TestRetrier):

    @pytest.fixture(params=[
        InvalidElementStateException,
        StaleElementReferenceException,
    ])
    def exception(self, request):
        return request.param

    @property
    def element_action_retrier(self) -> ElementActionRetrier:
        return ElementActionRetrier(self.retry_configuration)

    def test_retrier_should_be_possible__to_get_from_service(self):
        BrowserService.service_provider().element_action_retrier()

    def test_retrier_should_work_once(self):
        self.retrier_should_work_once(lambda: self.element_action_retrier.do_with_retry(lambda: None))

    def test_retrier_should_work_once_with_return(self):
        self.retrier_should_work_once(lambda: self.element_action_retrier.do_with_retry(lambda: 1))

    def test_retrier_should_wait_polling_interval(self, exception):
        throw_exception = [True]

        def predicate():
            if throw_exception[0]:
                throw_exception[0] = False
                raise exception

        self.retrier_should_wait_polling_interval(
            lambda: self.element_action_retrier.do_with_retry(predicate)
        )

    def test_retrier_should_wait_polling_interval_with_return(self, exception):
        throw_exception = [True]

        def predicate():
            if throw_exception[0]:
                throw_exception[0] = False
                raise exception
            return True

        self.retrier_should_wait_polling_interval(
            lambda: self.element_action_retrier.do_with_retry(predicate)
        )

    def test_retrier_should_throw__unhandled_exception(self):
        def predicate():
            raise ValueError

        try:
            self.element_action_retrier.do_with_retry(predicate, [])
        except ValueError:
            pass

    def test_retrier_should_work_correct_times(self, exception):
        actual_attempts = [0]

        def predicate():
            self.logger.info(f"current attempt is {actual_attempts[0]}")
            actual_attempts[0] += 1
            raise exception

        self.retrier_should_work_correct_times(
            exception,
            actual_attempts,
            lambda: self.element_action_retrier.do_with_retry(predicate, [exception]),
        )
