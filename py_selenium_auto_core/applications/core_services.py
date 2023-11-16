import abc
from typing import Callable, TypeVar

from py_selenium_auto_core.applications.application import Application
from py_selenium_auto_core.applications.startup import ServiceProvider, Startup

TServProv = TypeVar("TServProv", bound=ServiceProvider, covariant=True)
TApp = TypeVar("TApp", bound=Application, covariant=True)


class CoreServices(abc.ABC):
    _app_container: TApp = None
    _service_provider_container: TServProv = None

    @classmethod
    def _is_application_started(cls) -> bool:
        return cls._app_container is not None and cls._app_container.is_started

    @classmethod
    def _set_service_provider(cls, service_provider: TServProv):
        cls._service_provider_container = service_provider

    @classmethod
    def _get_service_provider(
        cls,
        application_provider: Callable[[TServProv], TApp],
        service_provider: Callable[[], TServProv] = None,
    ) -> TServProv:
        if cls._service_provider_container is None:
            if service_provider is not None:
                cls._service_provider_container = service_provider()
            elif cls._service_provider_container is None:
                cls._service_provider_container = Startup.configure_services(application_provider)
        return cls._service_provider_container

    @classmethod
    def _get_application(
        cls,
        application_provider: Callable[[TServProv], TApp],
        service_provider: Callable[[], TServProv] = None,
    ) -> TApp:
        if not cls._is_application_started():
            cls._app_container = application_provider(
                cls._get_service_provider(
                    lambda service: cls._get_application(application_provider, service_provider),
                    service_provider,
                )
            )
        return cls._app_container

    @classmethod
    def _set_application(cls, application: Application):
        cls._app_container = application
