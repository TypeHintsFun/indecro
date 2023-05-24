from abc import ABC
from dataclasses import dataclass
from datetime import datetime, timedelta

from indecro.api.rules import Rule
from indecro.exceptions import JobNeverBeScheduled


@dataclass
class IntervalRule(Rule):
    start: datetime
    period: timedelta

    def get_next_schedule_time(self, *, after: datetime) -> datetime:
        delta = after - self.start
        intervals = delta.total_seconds() // self.period.total_seconds() + 1
        return self.start + intervals * self.period

    def __repr__(self):
        # TODO: Remove hardcode from arguments displaying in repr
        return f'{self.__class__.__name__}(start={repr(self.start)}, period={repr(self.period)})'

    def __hash__(self):
        return hash(repr(self))


@dataclass
class SingleRun(Rule):
    when: datetime

    def get_next_schedule_time(self, *, after: datetime) -> datetime:
        if after > self.when:
            raise JobNeverBeScheduled(after=after, by_rule=self)
        return self.when

    def __repr__(self):
        # TODO: Remove hardcode from arguments displaying in repr
        return f'{self.__class__.__name__}(when={repr(self.when)})'

    def __hash__(self):
        return hash(repr(self))
