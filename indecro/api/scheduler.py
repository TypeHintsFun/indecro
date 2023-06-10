from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, Optional, Union, Awaitable, TYPE_CHECKING

if TYPE_CHECKING:
    from indecro.api.job import RunAs
    from indecro.api.job import Job

from indecro.api.task import Task
from indecro.api.rules import Rule


class Scheduler(Protocol):
    if TYPE_CHECKING:
        @abstractmethod
        def job(
                self,
                rule: Rule,

                daemonize: RunAs = RunAs.FUNCTION,

                name: Optional[str] = None,

                *args,
                **kwargs
        ):
            raise NotImplementedError()

        @abstractmethod
        def add_job(
                self,
                task: Task,
                rule: Rule,

                daemonize: RunAs = RunAs.FUNCTION,

                name: Optional[str] = None,

                *args,
                **kwargs
        ) -> Union[Job, Awaitable[Job]]:
            raise NotImplementedError()

        @abstractmethod
        async def execute_job(self, job: Job, reschedule: bool = True):
            raise NotImplementedError()

        @staticmethod
        @abstractmethod
        def schedule_job(job: Job):
            raise NotImplementedError()

        @abstractmethod
        def remove_job(self, job: Job):
            pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    async def run(self):
        raise NotImplementedError()
