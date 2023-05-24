from abc import abstractmethod
from asyncio import Protocol
from datetime import datetime


class Rule(Protocol):
    @abstractmethod
    def get_next_schedule_time(self, *, after: datetime) -> datetime:
        raise NotImplementedError()

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError()

    @abstractmethod
    def __hash__(self):
        raise NotImplementedError()
