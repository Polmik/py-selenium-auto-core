import pytest

from tests.applications.browser.browser_services import BrowserServices
from tests.applications.browser.test_with_browser import TestWithBrowser


class TestApplicationNotStarted(TestWithBrowser):

    service_provider_attrs = None

    def setup_method(self, method):
        super().setup_method(method)
        self.service_provider_attrs = self.service_provider.__dict__.get('providers')

    @pytest.mark.parametrize(
        'service',
        [
            "logger",
            "element_cache_configuration",
            "logger_configuration",
            "timeout_configuration",
            "retry_configuration",
            "localization_manager",
            "localized_logger",
            "action_retrier",
            "element_action_retrier",
            "conditional_wait",
            "element_finder",
        ]
    )
    def test_should_not_start_application(self, service):
        service_attr = self.service_provider.__getattribute__(service)
        assert service_attr is not None
        assert service_attr() is not None
        assert not BrowserServices.Instance.is_application_started()
