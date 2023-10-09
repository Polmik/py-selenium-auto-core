class TimeoutConfiguration:

    def __init__(self, settings_file):
        self.__settings_file = settings_file
        self.__timeout = self.__settings_file.get("timeouts")

    @property
    def implicit(self) -> float:
        return self.__timeout.get("timeout_implicit")

    @property
    def condition(self) -> float:
        return self.__timeout.get("timeout_condition")

    @property
    def polling_interval(self) -> float:
        return self.__timeout.get("timeout_polling_interval")

    @property
    def script(self) -> float:
        return self.__timeout.get("timeout_script")

    @property
    def page_load(self) -> float:
        return self.__timeout.get("timeout_page_load")

    @property
    def command(self) -> float:
        return self.__timeout.get("timeout_command")
