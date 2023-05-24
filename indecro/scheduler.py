import asyncio
import functools
from datetime import datetime
from typing import Optional, Union

from indecro.api.executor import Executor
from indecro.api.task import Task
from indecro.exceptions import JobNeverBeScheduled
from indecro.job import Job
from indecro.api.rules import Rule
from indecro.api.scheduler import Scheduler as SchedulerProtocol
from indecro.api.storage import Storage


class Scheduler(SchedulerProtocol):
    def __init__(self, storage: Storage, executor: Executor):
        self.storage = storage
        self.executor = executor

        self.running = False

    def task(
            self,
            rule: Rule,

            daemonize: bool = False,
            is_thread_safe: bool = False,

            name: Optional[str] = None,

            *args,
            **kwargs
    ):
        def decorator(task: Task):
            self.add_job(
                task=task,
                rule=rule,
                daemonize=daemonize,
                is_thread_safe=is_thread_safe,
                name=name,
                *args,
                **kwargs
            )
            return task

        return decorator

    def add_job(
            self,
            task: Task,
            rule: Rule,

            daemonize: bool = False,
            is_thread_safe: bool = False,

            name: Optional[str] = None,
            *args,
            **kwargs
    ) -> Job:
        if isinstance(task, Job):
            job = task
        else:
            job = Job(
                task=functools.partial(task, *args, **kwargs),
                rule=rule,
                next_run_time=rule.get_next_schedule_time(after=datetime.now()),
                name=name,
                scheduler=self,
                executor=self.executor,
                daemonize=daemonize,
                is_thread_safe=is_thread_safe
            )

        self.storage.add_job(job)

        return job

    async def stop(self):
        self.running = False

    async def execute_job(self, job: Job, reschedule: bool = True):
        job_executed = await self.executor.execute(job)

        if reschedule:
            self.schedule_job(job)

        return job_executed

    @staticmethod
    def schedule_job(job: Job):
        job.next_run_time = job.rule.get_next_schedule_time(after=datetime.now())
        return job.next_run_time

    async def remove_job(self, job: Job):
        self.storage.remove_job(job)

    async def run(self):
        self.running = True
        while self.running:
            now = datetime.now()

            any_job_started = False
            # print(f'{now=}')
            for job in self.storage.iter_jobs(before=now):
                try:
                    job_executed = await self.execute_job(job)
                except JobNeverBeScheduled:
                    self.storage.remove_job(job)
                    job_executed = False

                any_job_started = job_executed or any_job_started

            await asyncio.sleep(not any_job_started)
