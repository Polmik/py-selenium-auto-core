class ElementCacheConfiguration:

    def __init__(self, settings_file):
        self.__settings_file = settings_file
        self.__element_cache = self.__settings_file.get("element_cache")

    @property
    def is_enabled(self) -> bool:
        return self.__element_cache.get("is_enabled")
