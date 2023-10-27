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
from python_selenium_core.utilities.root_path_helper import RootPathHelper
from python_selenium_core.utilities.element_action_retrier import ElementActionRetrier
from python_selenium_core.utilities.environment_configuration import EnvironmentConfiguration
from python_selenium_core.utilities.file_reader import FileReader
from python_selenium_core.elements.element_finder import ElementFinder
from python_selenium_core.utilities.json_settings_file import JsonSettingsFile
from python_selenium_core.waitings.conditional_wait import ConditionalWait


class ServiceProvider(containers.DeclarativeContainer):
    """Container that allows to resolve dependencies for all services in the library"""
    __self__ = Self()

    settings_file: Singleton[JsonSettingsFile] = Singleton(lambda: JsonSettingsFile({}))
    application: Factory[Application] = Factory(Application)
    logger: Singleton[Logger] = Singleton(Logger)
    element_cache_configuration: Singleton[ElementCacheConfiguration] = Singleton(
        ElementCacheConfiguration,
        settings_file,
    )
    logger_configuration: Singleton[LoggerConfiguration] = Singleton(LoggerConfiguration, settings_file)
    timeout_configuration: Singleton[TimeoutConfiguration] = Singleton(TimeoutConfiguration, settings_file)
    retry_configuration: Singleton[RetryConfiguration] = Singleton(RetryConfiguration, settings_file)
    localization_manager: Singleton[LocalizationManager] = Singleton(LocalizationManager, logger_configuration, logger)
    localized_logger: Singleton[LocalizedLogger] = Singleton(
        LocalizedLogger,
        localization_manager,
        logger,
        logger_configuration,
    )
    action_retrier: Singleton[ActionRetrier] = Singleton(ActionRetrier, retry_configuration)
    element_action_retrier: Singleton[ElementActionRetrier] = Singleton(ElementActionRetrier, retry_configuration)
    conditional_wait: Factory[ConditionalWait] = Factory(ConditionalWait, timeout_configuration, __self__)
    element_finder: Factory[ElementFinder] = Factory(ElementFinder, localized_logger, conditional_wait)


class Startup:

    @staticmethod
    def configure_services(application_provider: Callable, settings: JsonSettingsFile = None) -> ServiceProvider:
        """Method to configure dependencies for services of the current library

        Args:
            application_provider: Provider for interacting with the application
                Example: lambda: Application.get_application()
            settings: File with settings for configuration of dependencies
                Pass the result of get_settings() if you need to get settings from the another package

        Returns:
            Configured ServiceProvider
        """
        service_provider = ServiceProvider()
        settings = settings or Startup.get_settings()

        service_provider.settings_file.override(Singleton(lambda: settings))
        service_provider.application.override(Factory(application_provider))

        return service_provider

    @staticmethod
    def get_settings() -> JsonSettingsFile:
        """Provides a JsonSettingsFile with settings. Value is set in configure_services
        Otherwise, will use default JSON settings file with name: "settings.{profile}.json".
        Default settings will look for the resource file in resource file (FileReader);
         If not found, will look for resource in the calling package of this method

        Returns:
            An instance of settings
        """
        profile_name = EnvironmentConfiguration.get_variable("profile")
        settings_profile = "settings.json" if not profile_name else f"settings.{profile_name}.json"
        Logger.debug(f"Get settings from: {settings_profile}")
        if FileReader.is_resource_file_exist(settings_profile, root_path=RootPathHelper.calling_root_path()):
            return JsonSettingsFile(setting_name=settings_profile, root_path=RootPathHelper.calling_root_path())
        return JsonSettingsFile(setting_name=settings_profile, root_path=RootPathHelper.executing_root_path())
