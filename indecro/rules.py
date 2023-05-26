from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Callable, Any, Union

from magic_filter import MagicFilter

from indecro.api.rules import Rule, BoolRule
from indecro.exceptions import JobNeverBeScheduled


@dataclass
class RunEvery(Rule):
    period: timedelta
    after: datetime = field(default_factory=datetime.now)
    before: Optional[datetime] = None
    repeats: Optional[int] = None

    def get_next_schedule_time(self, *, after: datetime) -> datetime:
        delta = after - self.after
        intervals = delta.total_seconds() // self.period.total_seconds() + 1

        next_schedule_time = self.after + intervals * self.period

        if self.before is not None and self.before <= next_schedule_time:
            raise JobNeverBeScheduled(after=after, by_rule=self)

        if self.repeats is not None and self.repeats < intervals:
            raise JobNeverBeScheduled(after=after, by_rule=self)

        return next_schedule_time

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


@dataclass
class RunWhen(BoolRule):
    will: Union[MagicFilter, Callable[[], bool]]
    subject: Union[None, Any] = None

    def get_must_be_scheduled_now_flag(self):
        if isinstance(self.will, MagicFilter):
            return self.will.resolve(self.subject)
        elif isinstance(self.will, Callable):
            return self.will()

    def __repr__(self):
        # TODO: Remove hardcode from arguments displaying in repr
        return f'{self.__class__.__name__}(at={repr(self.will)}, after={self.subject})'

    def __hash__(self):
        return hash(repr(self))
