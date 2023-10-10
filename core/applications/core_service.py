from typing import Callable

from dependency_injector import providers

from core.applications.iapplication import Application
from core.applications.startup import ServiceProvider, Startup


#class CoreService(Application):
class CoreService:

    _app_container: Application = None
    _startup_container: ServiceProvider = None

    @staticmethod
    def _is_application_started() -> bool:
        return CoreService._app_container is not None and CoreService._app_container.is_started

    @staticmethod
    def set_service_provider(startup: ServiceProvider):
        CoreService._startup_container = startup

    @staticmethod
    def get_service_provider(application_provider: Callable, service_provider: ServiceProvider = None) -> ServiceProvider:
        if CoreService._startup_container is None:
            if service_provider is None:
                CoreService._startup_container = Startup.configure_services(application_provider)
                CoreService._startup_container.application = providers.Factory(application_provider)
            else:
                CoreService._startup_container = service_provider
        return CoreService._startup_container

    @staticmethod
    def get_application(application_provider: Callable, service_provider: ServiceProvider = None):
        if not CoreService._is_application_started():
            CoreService._app_container = application_provider(
                CoreService.get_service_provider(lambda x: CoreService.get_application(application_provider, service_provider), service_provider)
            )
        return CoreService._app_container

    @staticmethod
    def set_application(application: Application):
        CoreService._app_container = application

