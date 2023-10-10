class LoggerConfiguration:

    __default_language = "en"

    def __init__(self, settings_file):
        self.__settings_file = settings_file
        self.__logger = self.__settings_file.get("logger")

    @property
    def language(self) -> str:
        return self.__logger.get("language", self.__default_language)

    @property
    def log_page_source(self) -> bool:
        return self.__logger.get("logPageSource", True)
