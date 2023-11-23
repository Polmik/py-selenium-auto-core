import abc
from typing import Callable, TypeVar

from py_selenium_auto_core.applications.application import Application
from py_selenium_auto_core.applications.startup import ServiceProvider, Startup

_TServProv = TypeVar("_TServProv", bound=ServiceProvider, covariant=True)
_TApp = TypeVar("_TApp", bound=Application, covariant=True)


class CoreServices(abc.ABC):
    _app_container: _TApp = None
    _service_provider_container: _TServProv = None

    @classmethod
    def _is_application_started(cls) -> bool:
        return cls._app_container is not None and cls._app_container.is_started

    @classmethod
    def _set_service_provider(cls, service_provider: _TServProv):
        cls._service_provider_container = service_provider

    @classmethod
    def _get_service_provider(
        cls,
        application_provider: Callable[[_TServProv], _TApp],
        service_provider: Callable[[], _TServProv] = None,
    ) -> _TServProv:
        if cls._service_provider_container is None:
            if service_provider is not None:
                cls._service_provider_container = service_provider()
            elif cls._service_provider_container is None:
                cls._service_provider_container = Startup.configure_services(application_provider)
        return cls._service_provider_container

    @classmethod
    def _get_application(
        cls,
        application_provider: Callable[[_TServProv], _TApp],
        service_provider: Callable[[], _TServProv] = None,
    ) -> _TApp:
        if not cls._is_application_started():
            cls._app_container = application_provider(
                cls._get_service_provider(
                    lambda service: cls._get_application(application_provider, service_provider),
                    service_provider,
                )
            )
        return cls._app_container

    @classmethod
    def _set_application(cls, application: _TApp):
        cls._app_container = application
