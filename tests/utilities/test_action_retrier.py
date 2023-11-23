from py_selenium_auto_core.utilities.action_retrier import ActionRetrier
from tests.applications.browser.browser_services import BrowserServices
from tests.utilities.test_retrier import TestRetrier


class TestActionRetrier(TestRetrier):
    handled_exceptions = [ValueError]

    @property
    def action_retrier(self):
        return ActionRetrier(self.retry_configuration)

    def test_retrier_should_be_possible__to_get_from_service(self):
        BrowserServices.Instance.service_provider.action_retrier()

    def test_retrier_should_work_once(self):
        self.retrier_should_work_once(lambda: self.action_retrier.do_with_retry(lambda: None))

    def test_retrier_should_work_once_with_return(self):
        self.retrier_should_work_once(lambda: self.action_retrier.do_with_retry(lambda: 1))

    def test_retrier_should_wait_polling_interval(self):
        throw_exception = [True]

        def _predicate():
            if throw_exception[0]:
                throw_exception[0] = False
                raise ValueError

        self.retrier_should_wait_polling_interval(
            lambda: self.action_retrier.do_with_retry(_predicate, self.handled_exceptions)
        )

    def test_retrier_should_wait_polling_interval_with_return(self):
        throw_exception = [True]

        def _predicate():
            if throw_exception[0]:
                throw_exception[0] = False
                raise ValueError
            return True

        self.retrier_should_wait_polling_interval(
            lambda: self.action_retrier.do_with_retry(_predicate, self.handled_exceptions)
        )

    def test_retrier_should_throw__unhandled_exception(self):
        def _predicate():
            raise ValueError

        try:
            self.action_retrier.do_with_retry(_predicate, [])
        except ValueError:
            pass

    def test_retrier_should_work_correct_times(self):
        actual_attempts = [0]

        def _predicate():
            self.logger.info(f"current attempt is {actual_attempts[0]}")
            actual_attempts[0] += 1
            raise ValueError

        self.retrier_should_work_correct_times(
            ValueError,
            actual_attempts,
            lambda: self.action_retrier.do_with_retry(_predicate, self.handled_exceptions),
        )
