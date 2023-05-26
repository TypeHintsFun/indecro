from abc import ABC
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from indecro.api.rules import Rule
from indecro.exceptions import JobNeverBeScheduled


@dataclass
class RunEvery(Rule):
    period: timedelta
    after: datetime = field(default_factory=datetime.now)

    def get_next_schedule_time(self, *, after: datetime) -> datetime:
        delta = after - self.after
        intervals = delta.total_seconds() // self.period.total_seconds() + 1
        return self.after + intervals * self.period

    def __repr__(self):
        # TODO: Remove hardcode from arguments displaying in repr
        return f'{self.__class__.__name__}(start={repr(self.after)}, period={repr(self.period)})'

    def __hash__(self):
        return hash(repr(self))


@dataclass(init=False)
class RunOnce(Rule):
    at: Optional[datetime] = None
    after: Optional[timedelta] = None

    def __init__(
            self,
            at: Optional[datetime] = None,
            after: Optional[timedelta] = None
    ):
        if (not at) and (not after):
            raise ValueError('You must provide at parameter or after parameter')

        if at is None:
            at = datetime.now() + after

        self.at = at
        self.after = after

    def get_next_schedule_time(self, *, after: datetime) -> datetime:
        if after > self.at:
            raise JobNeverBeScheduled(after=after, by_rule=self)
        return self.at

    def __repr__(self):
        # TODO: Remove hardcode from arguments displaying in repr
        return f'{self.__class__.__name__}(at={repr(self.at)}, after={self.after})'

    def __hash__(self):
        return hash(repr(self))
