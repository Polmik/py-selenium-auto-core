import json
from typing import Callable

from dependency_injector import containers
from dependency_injector.providers import Singleton, Factory, Self

from python_selenium_core.applications.application import Application
from python_selenium_core.configurations.element_cache_configuration import ElementCacheConfiguration
from python_selenium_core.configurations.logger_configuration import LoggerConfiguration
from python_selenium_core.configurations.retry_configuration import RetryConfiguration
from python_selenium_core.configurations.timeout_configuration import TimeoutConfiguration
from python_selenium_core.localization.localization_manager import LocalizationManager
from python_selenium_core.localization.localized_logger import LocalizedLogger
from python_selenium_core.logging.logger import Logger
from python_selenium_core.utilities.action_retrier import ActionRetrier
from python_selenium_core.utilities.element_action_retrier import ElementActionRetrier
from python_selenium_core.utilities.file_reader import FileReader
from python_selenium_core.elements.element_finder import ElementFinder
from python_selenium_core.waitings.conditional_wait import ConditionalWait


class ServiceProvider(containers.DeclarativeContainer):
    __self__ = Self()

    settings_file: Singleton[dict] = Singleton(lambda: {})
    application: Factory[Application] = Factory(Application)
    logger: Singleton[Logger] = Singleton(Logger)
    element_cache_configuration: Singleton[ElementCacheConfiguration] = Singleton(ElementCacheConfiguration, settings_file)
    logger_configuration: Singleton[LoggerConfiguration] = Singleton(LoggerConfiguration, settings_file)
    timeout_configuration: Singleton[TimeoutConfiguration] = Singleton(TimeoutConfiguration, settings_file)
    retry_configuration: Singleton[RetryConfiguration] = Singleton(RetryConfiguration, settings_file)
    localization_manager: Singleton[LocalizationManager] = Singleton(LocalizationManager, logger_configuration, logger)
    localized_logger: Singleton[LocalizedLogger] = Singleton(LocalizedLogger, localization_manager, logger, logger_configuration)
    action_retrier: Singleton[ActionRetrier] = Singleton(ActionRetrier, retry_configuration)
    element_action_retrier: Singleton[ElementActionRetrier] = Singleton(ElementActionRetrier, retry_configuration)
    conditional_wait: Factory[ConditionalWait] = Factory(ConditionalWait, timeout_configuration, __self__)
    element_finder: Factory[ElementFinder] = Factory(ElementFinder, localized_logger, conditional_wait)


class Startup:

    @staticmethod
    def configure_services(application_provider: Callable, settings: dict = None) -> ServiceProvider:
        service_provider = ServiceProvider()
        settings = settings or json.loads(FileReader.get_resource_file("settings.json"))

        service_provider.settings_file.override(Singleton(lambda: settings))
        service_provider.application.override(Factory(application_provider))

        return service_provider
