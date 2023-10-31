# Selenium CORE for Python

[![Tests](https://github.com/Polmik/python-selenium-core/actions/workflows/tests.yml/badge.svg)](https://github.com/Polmik/python-selenium-core/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/Polmik/python-selenium-core/branch/main/graph/badge.svg)](https://codecov.io/gh/Polmik/python-selenium-core)

### Introduction

It's a library with core functions simplifying work with Selenium-controlled applications.

This package is based on **Aquality Selenium CORE for .NET** and provides a set of methods related to the most common actions performed with elements. So you shouldn't have a lot of difficulties with this solution if you interacted with **Aquality Selenium CORE**.

To simplify overriding of implementations this solution uses Dependency Injection.

### Supported Python Versions

* Python 3.7-3.9

### Installation 

If you have [pip](https://pip.pypa.io/en/stable/) on your system, you can simply install or upgrade the Python bindings:

```bash
pip install -U selenium
```

Alternately, you can download the source distribution from [PyPI](https://pypi.org/project/python-selenium-core/#files), unarchive it, and run:

```bash
python setup.py install
```

### Quick start

1. Setup Dependency Injection container using Startup

The simplest way is to create your own Services class extended from abstract CoreServices with the following simple signature:

```python
class BrowserService(CoreService):

    @staticmethod
    def is_application_started() -> bool:
        return CoreService._is_application_started()

    @staticmethod
    def application() -> YourApplication:
        return CoreService.get_application(lambda service: BrowserService._start_application(service))

    @staticmethod
    def service_provider() -> ServiceProvider:
        return CoreService.get_service_provider(lambda service: BrowserService.application())

    @staticmethod
    def _start_application(service_provider: ServiceProvider):
        ...  # your implementation
```

If you need to register your own services / rewrite the implementation, you need override Startup and implement BrowserServices like in example below:

```python
class BrowserService(CoreService):
    
    _browser_startup_container: CustomStartup = CustomStartup()
    
    @staticmethod
    def is_application_started() -> bool:
        return CoreService._is_application_started()

    @staticmethod
    def application() -> Application:
        return CoreService.get_application(lambda service: your_implementation, lambda: BrowserService._browser_startup_container.configure_services(lambda service: BrowserService.application()))

    @staticmethod
    def service_provider() -> ServiceProvider:
        return CoreService.get_service_provider(lambda service: BrowserService.application())

    @staticmethod
    def _start_application(service_provider: ServiceProvider):
        ...  # your implementation
    
    
class CustomStartup(Startup):

    @staticmethod
    def configure_services(application_provider: Callable, settings: JsonSettingsFile = None) -> ServiceProvider:
        service_provider = Startup.configure_services(application_provider, settings)
        # your implementation service_provider.timeout_configuration.override(Singleton(TimeoutConfiguration, service_provider.settings_file))
        return service_provider
```

2. Work with Application via the implemented BrowserServices or via element services

All the services could be resolved from the Dependency Injection container via ServiceProvider
```python
BrowserServices.application().driver.find_element(ELEMENT).click()
BrowserServices.service_provider().conditional_wait().wait_for_driver(
    lambda driver: len(driver.find_elements(Locator(By.XPATH, "//*"))) > 0
)
```


### License
Library's source code is made available under the [Apache 2.0 license](https://github.com/Polmik/python-selenium-core/blob/main/LICENSE).