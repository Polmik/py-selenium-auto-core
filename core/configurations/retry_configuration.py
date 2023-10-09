class RetryConfiguration:

    def __init__(self, settings_file):
        self.__settings_file = settings_file
        self.__retry = self.__settings_file.get("retry")

    @property
    def number(self) -> int:
        return self.__retry.get("number")

    @property
    def polling_interval(self) -> int:
        return self.__retry.get("polling_interval")
