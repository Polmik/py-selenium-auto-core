import logging
import os

from pathlib import Path
from threading import Lock


class SingletonMeta(type):
    """
    Это потокобезопасная реализация класса Singleton.
    """

    _instances = {}

    _lock: Lock = Lock()
    """
    У нас теперь есть объект-блокировка для синхронизации потоков во время
    первого доступа к Одиночке.
    """

    def __call__(cls, *args, **kwargs):
        """
        Данная реализация не учитывает возможное изменение передаваемых
        аргументов в `__init__`.
        """
        # Теперь представьте, что программа была только-только запущена.
        # Объекта-одиночки ещё никто не создавал, поэтому несколько потоков
        # вполне могли одновременно пройти через предыдущее условие и достигнуть
        # блокировки. Самый быстрый поток поставит блокировку и двинется внутрь
        # секции, пока другие будут здесь его ожидать.
        with cls._lock:
            # Первый поток достигает этого условия и проходит внутрь, создавая
            # объект-одиночку. Как только этот поток покинет секцию и освободит
            # блокировку, следующий поток может снова установить блокировку и
            # зайти внутрь. Однако теперь экземпляр одиночки уже будет создан и
            # поток не сможет пройти через это условие, а значит новый объект не
            # будет создан.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Logger(metaclass=SingletonMeta):
    __log = None

    @classmethod
    def _instance(cls):
        if cls.__log is None:
            cls.__log = logging.getLogger()
            cls.__configure_logger()
        return cls.__log

    @classmethod
    def info(cls, msg):
        cls._instance().info(msg)

    @classmethod
    def debug(cls, msg, exc_info: Exception = None):
        cls._instance().debug(msg, exc_info=exc_info)

    @classmethod
    def warn(cls, msg):
        cls._instance().warn(msg)

    @classmethod
    def error(cls, msg):
        cls._instance().error(msg)

    @classmethod
    def fatal(cls, msg):
        cls._instance().fatal(msg)

    @classmethod
    def __configure_logger(cls):
        log_path = os.path.join(Path(__file__).parent.parent.parent, "Log\\log.log")

        if not os.path.exists(os.path.dirname(log_path)):
            os.mkdir(os.path.dirname(log_path))

        cls.__log.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        logging.getLogger().addHandler(stream_handler)
        logging.getLogger().addHandler(file_handler)
