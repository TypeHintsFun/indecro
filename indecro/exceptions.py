from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from indecro.api.job import Job
from indecro.api.rules import Rule


# TODO: Add an repr for all exceptions


# root exception, bounded to rule
class RuleException(Exception):
    def __init__(self, rule: Rule):
        self.rule = rule

        super().__init__()


# root exception, bounded to scheduler work
class SchedulerException(Exception):
    if TYPE_CHECKING:
        def __init__(self, job: Job):
            self.job = job


# Cannot do smth bounded with rule
class RuleCannotSmthException(RuleException):
    def __init__(self, *, after: datetime, by_rule: Rule):
        super().__init__(rule=by_rule)

        self.after = after
        self.by_rule = by_rule

    def __repr__(self):
        return f'{self.__class__.__name__}(after={self.after}, by_rule={self.by_rule})'


# At main, for BoolRule
class CannotPredictJobSchedulingTime(RuleCannotSmthException):
    pass


# For SingleRun and other similar rules
class JobNeverBeScheduled(RuleCannotSmthException):
    pass
