from typing import Callable, Optional

import pytest
from dependency_injector.providers import Singleton

from py_selenium_auto_core.applications.application import Application
from py_selenium_auto_core.applications.core_services import CoreServices
from py_selenium_auto_core.applications.startup import Startup, ServiceProvider
from py_selenium_auto_core.configurations.logger_configuration import (
    LoggerConfiguration,
)
from py_selenium_auto_core.configurations.timeout_configuration import (
    TimeoutConfiguration,
)
from py_selenium_auto_core.logging.logger import Logger
from py_selenium_auto_core.utilities.json_settings_file import JsonSettingsFile
from py_selenium_auto_core.utilities.root_path_helper import RootPathHelper


@pytest.fixture
def reset_override(request):
    request.addfinalizer(lambda: ServiceProvider.reset_override())
    yield


class TestCoreServices:
    def test_register_custom_services_via_startup(self):
        assert isinstance(
            TestBrowserService.Instance.service_provider.timeout_configuration(),
            TestTimeoutConfiguration,
        )

    def test_get_custom_values_via_startup(self):
        timeout_configuration: TestTimeoutConfiguration = (
            TestBrowserService.Instance.service_provider.timeout_configuration()
        )
        assert timeout_configuration.custom_timeout == 656
        assert timeout_configuration.polling_interval == 1
        # Check overriding for related classes
        assert TestBrowserService.Instance.service_provider.conditional_wait()._resolve_polling_interval(None) == 1

    @pytest.mark.skip(reason="Incorrect overriding of logger using set_startup")
    def test_get_custom_logger_values_via_startup(self):
        TestBrowserService.Instance.set_startup(CustomStartup())
        logger_configuration: CustomLoggerConfiguration = (
            TestBrowserService.Instance.service_provider.logger_configuration()
        )
        assert logger_configuration.custom_logger == "CustomLogger"

    def test_register_custom_services_via_startup_with_custom_settings_file(
        self,
    ):
        assert "special" == TestBrowserService.Instance.service_provider.logger_configuration().language

    def test_set_correct_value_for_new_instance_sp_after_overriding(self):
        assert type(CustomServiceProvider.timeout_configuration) == Singleton[TestTimeoutConfiguration]

    def test_set_correct_implementation_for_related_objects_after_overriding(self):
        service_provider = CustomSPStartup.configure_services(lambda: None)
        assert service_provider.timeout_configuration().custom_timeout == 656
        assert service_provider.timeout_configuration().polling_interval == 1
        # Check overriding for related classes
        assert service_provider.conditional_wait()._resolve_polling_interval(None) == 1

    def test_overriding_not_affect_base_implementation(self):
        service_provider = CustomSPStartup.configure_services(lambda: None)
        assert service_provider.timeout_configuration().custom_timeout == 656
        assert service_provider.timeout_configuration().polling_interval == 1
        # Check overriding for related classes
        assert service_provider.conditional_wait()._resolve_polling_interval(None) == 1

        base_service_provider = Startup.configure_services(lambda: None)
        assert base_service_provider.timeout_configuration().polling_interval == 0.3
        # Check overriding for related classes
        assert base_service_provider.conditional_wait()._resolve_polling_interval(None) == 0.3

    def test_custom_provider_not_set_implementation_for_related_without_overriding(
        self,
    ):
        service_provider = CustomSPStartup.configure_services_without_override(lambda: None)
        assert service_provider.timeout_configuration().custom_timeout == 656
        assert service_provider.timeout_configuration().polling_interval == 1
        # Check overriding for related classes
        assert service_provider.conditional_wait()._resolve_polling_interval(None) == 0.3


class TestStartup(Startup):
    @classmethod
    def configure_services(
        cls,
        application_provider: Callable,
        settings: Optional[JsonSettingsFile] = None,
        service_provider: Optional[ServiceProvider] = None,
    ) -> ServiceProvider:
        settings = JsonSettingsFile("settings.special.json", RootPathHelper.calling_root_path())
        service_provider = super().configure_services(application_provider, settings)
        service_provider.timeout_configuration.override(
            Singleton(TestTimeoutConfiguration, service_provider.settings_file)
        )
        return service_provider


class CustomStartup(TestStartup):
    @staticmethod
    def configure_services(
        application_provider: Callable,
        settings: Optional[JsonSettingsFile] = None,
        service_provider: Optional[ServiceProvider] = None,
    ) -> ServiceProvider:
        settings = JsonSettingsFile("settings.special.json", RootPathHelper.calling_root_path())
        service_provider = TestStartup.configure_services(application_provider, settings)
        service_provider.logger_configuration.override(
            Singleton(CustomLoggerConfiguration, service_provider.settings_file)
        )
        return service_provider


class TestTimeoutConfiguration(TimeoutConfiguration):
    def __init__(self, settings):
        super().__init__(settings)
        self._custom_timeout = 656

    @property
    def custom_timeout(self):
        return self._custom_timeout

    @property
    def polling_interval(self) -> float:
        return 1


class CustomLoggerConfiguration(LoggerConfiguration):
    def __init__(self, settings):
        super().__init__(settings)
        self._custom_timeout = "CustomLogger"

    @property
    def custom_logger(self):
        return self._custom_timeout


class TestBrowserService:
    class BrowserService(CoreServices):
        startup: TestStartup = TestStartup()

        def __init__(self):
            Logger.info("Create")

        @property
        def application(self) -> Application:
            return self._get_application(
                self._start_function,
                lambda: self.startup.configure_services(lambda service: self.application),
            )

        @property
        def service_provider(self) -> ServiceProvider:
            return self._get_service_provider(
                lambda service: self.application,
                lambda: self.startup.configure_services(lambda service: self.application),
            )

        def set_startup(self, startup: Startup):
            if startup is not None:
                self.startup = startup

        @property
        def _start_function(self):
            def _predicate(service):
                raise NotImplementedError

            return _predicate

    Instance: BrowserService = BrowserService()


class CustomServiceProvider(ServiceProvider):
    timeout_configuration: Singleton[TimeoutConfiguration] = Singleton(
        TestTimeoutConfiguration, ServiceProvider.settings_file
    )


class CustomSPStartup(Startup):
    @classmethod
    def configure_services(
        cls,
        application_provider: Callable,
        settings: Optional[JsonSettingsFile] = None,
        service_provider: Optional[ServiceProvider] = None,
    ) -> CustomServiceProvider:
        ServiceProvider.override(CustomServiceProvider)

        settings = JsonSettingsFile("settings.special.json", RootPathHelper.calling_root_path())
        service_provider = super().configure_services(application_provider, settings, CustomServiceProvider())

        ServiceProvider.reset_override()
        return service_provider

    @classmethod
    def configure_services_without_override(
        cls,
        application_provider: Callable,
    ) -> CustomServiceProvider:
        settings = JsonSettingsFile("settings.special.json", RootPathHelper.calling_root_path())
        service_provider = super().configure_services(application_provider, settings, CustomServiceProvider())
        return service_provider
