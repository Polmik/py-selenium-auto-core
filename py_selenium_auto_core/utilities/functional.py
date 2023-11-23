from datetime import timedelta, datetime


class Timer:
    @property
    def elapsed(self) -> timedelta:
        return self.end_date - self.start_time

    def __enter__(self) -> "Timer":
        self.start_time = datetime.now()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_date = datetime.now()
        return True
