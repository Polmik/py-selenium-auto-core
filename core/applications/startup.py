import json
from typing import Callable

from dependency_injector import containers
from dependency_injector.providers import Singleton, Factory

from core.applications.iapplication import Application
from core.configurations.element_cache_configuration import ElementCacheConfiguration
from core.configurations.logger_configuration import LoggerConfiguration
from core.configurations.retry_configuration import RetryConfiguration
from core.configurations.timeout_configuration import TimeoutConfiguration
from core.localization.localization_manager import LocalizationManager
from core.localization.localized_logger import LocalizedLogger
from core.logging.logger import Logger
from core.utilities.action_retrier import ActionRetrier
from core.utilities.element_action_retrier import ElementActionRetrier
from core.utilities.file_reader import FileReader
from core.elements.element_finder import ElementFinder
from core.waitings.conditional_wait import ConditionalWait


class ServiceProvider(containers.DeclarativeContainer):
    settings_file: Singleton[dict] = Singleton(lambda: json.loads(FileReader.get_resource_file("settings.json")))
    application: Factory[Application] = None
    logger: Singleton[Logger] = Singleton(Logger)
    element_cache_configuration: Singleton[ElementCacheConfiguration] = Singleton(ElementCacheConfiguration, settings_file)
    logger_configuration: Singleton[LoggerConfiguration] = Singleton(LoggerConfiguration, settings_file)
    timeout_configuration: Singleton[TimeoutConfiguration] = Singleton(TimeoutConfiguration, settings_file)
    retry_configuration: Singleton[RetryConfiguration] = Singleton(RetryConfiguration, settings_file)
    localization_manager: Singleton[LocalizationManager] = Singleton(LocalizationManager, logger_configuration, logger)
    localized_logger: Singleton[LocalizedLogger] = Singleton(LocalizedLogger, localization_manager, logger, logger_configuration)
    action_retrier: Singleton[ActionRetrier] = Singleton(ActionRetrier, retry_configuration)
    element_action_retrier: Singleton[ElementActionRetrier] = Singleton(ElementActionRetrier, retry_configuration)
    conditional_wait: Factory[ConditionalWait] = Factory(ConditionalWait, timeout_configuration, application)
    element_finder: Factory[ElementFinder] = Factory(ElementFinder, conditional_wait)


class Startup:

    @staticmethod
    def configure_services(application_provider: Callable, settings: dict = None) -> ServiceProvider:
        service_provider = ServiceProvider()
        settings = settings or json.loads(FileReader.get_resource_file("settings.json"))
        service_provider.settings_file = Singleton(lambda: settings)
        service_provider.application = Factory(application_provider)
        return service_provider
