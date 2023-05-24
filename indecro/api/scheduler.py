from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, Optional, Union, Any, Awaitable

from indecro.api.task import Task
from indecro.api.rules import Rule


@dataclass
class Job:
    task: Task
    rule: Rule
    next_run_time: datetime
    name: Optional[str] = None
    scheduler: Optional[Scheduler] = None

    @abstractmethod
    async def schedule(self) -> Any:
        raise NotImplementedError()


class Scheduler(Protocol):
    @abstractmethod
    def task(
            self,
            rule: Rule,

            daemonize: bool = False,
            is_thread_safe: bool = False,

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

            daemonize: bool = False,
            is_thread_safe: bool = False,

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
    async def stop(self):
        pass

    @abstractmethod
    async def run(self):
        raise NotImplementedError()
