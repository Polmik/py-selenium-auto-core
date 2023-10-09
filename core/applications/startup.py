import json

from dependency_injector import containers, providers

from core.configurations.element_cache_configuration import ElementCacheConfiguration
from core.configurations.logger_configuration import LoggerConfiguration
from core.configurations.retry_configuration import RetryConfiguration
from core.configurations.timeout_configuration import TimeoutConfiguration
from core.localization.localization_manager import LocalizationManager
from core.localization.localized_logger import LocalizedLogger
from core.logging.logger import Logger
from core.utilities.file_reader import FileReader


class Startup(containers.DeclarativeContainer):
    settings_file: dict = providers.Singleton(lambda: json.loads(FileReader.get_resource_file("settings.json")))
    logger: Logger = providers.Singleton(Logger)
    element_cache_configuration: ElementCacheConfiguration = providers.Singleton(ElementCacheConfiguration, settings_file)
    logger_configuration: LoggerConfiguration = providers.Singleton(LoggerConfiguration, settings_file)
    timeout_configuration: TimeoutConfiguration = providers.Singleton(TimeoutConfiguration, settings_file)
    retry_configuration: RetryConfiguration = providers.Singleton(RetryConfiguration, settings_file)
    localization_manager: LocalizationManager = providers.Singleton(LocalizationManager, logger_configuration, logger)
    localized_logger: LocalizedLogger = providers.Singleton(LocalizedLogger, localization_manager, logger, logger_configuration)

