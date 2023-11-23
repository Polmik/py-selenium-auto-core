import abc


class CoreForm(abc.ABC):
    @property
    @abc.abstractmethod
    def name(self) -> str:
        raise NotImplementedError("Abstract")

    @property
    @abc.abstractmethod
    def _localized_logger(self):
        raise NotImplementedError("Abstract")
