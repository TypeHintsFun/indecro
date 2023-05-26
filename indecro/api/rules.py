from abc import abstractmethod
from asyncio import Protocol
from datetime import datetime

from typing import NoReturn


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


class BoolRule(Rule, Protocol):
    @abstractmethod
    def get_must_be_scheduled_now_flag(self):
        raise NotImplementedError()

    def get_next_schedule_time(self, *, after: datetime) -> NoReturn:
        from indecro.exceptions import CannotPredictJobSchedulingTime

        raise CannotPredictJobSchedulingTime(after=after, by_rule=self)
