from typing import Callable

from dependency_injector import providers

from python_selenium_core.applications.application import Application
from python_selenium_core.applications.startup import ServiceProvider, Startup


class CoreService:

    _app_container: Application = None
    _service_provider_container: ServiceProvider = None

    @classmethod
    def _is_application_started(cls) -> bool:
        return CoreService._app_container is not None and CoreService._app_container.is_started

    @classmethod
    def set_service_provider(cls, startup: ServiceProvider):
        CoreService._service_provider_container = startup

    @classmethod
    def get_service_provider(
            cls,
            application_provider: Callable,
            service_provider: ServiceProvider = None
    ) -> ServiceProvider:
        if CoreService._service_provider_container is None:
            if service_provider is None:
                CoreService._service_provider_container = Startup.configure_services(application_provider)
                CoreService._service_provider_container.application = providers.Factory(application_provider)
            else:
                CoreService._service_provider_container = service_provider
        return CoreService._service_provider_container

    @classmethod
    def get_application(cls, application_provider: Callable, service_provider: ServiceProvider = None):
        if not CoreService._is_application_started():
            CoreService._app_container = application_provider(
                CoreService.get_service_provider(
                    lambda x: CoreService.get_application(application_provider, service_provider), service_provider
                )
            )
        return CoreService._app_container

    @classmethod
    def set_application(cls, application: Application):
        CoreService._app_container = application
