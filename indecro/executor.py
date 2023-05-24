import asyncio
import functools
from typing import Awaitable, Any, Union, Coroutine, Callable

from indecro.api.executor import Executor as ExecutorProtocol
from indecro.api.job import Job


class Executor(ExecutorProtocol):
    def __init__(self):
        self.daemonized_tasks: set[asyncio.Task] = set()

    async def execute(self, job: Job):
        if job.is_running:
            return False

        if job.daemonize:
            if job.is_thread_safe:
                res = asyncio.to_thread(functools.partial(self.sync_worker, job.task, job))
            else:
                res = job.task()

                if not isinstance(res, Awaitable):
                    pass
                    # TODO: Create warning message here

                if isinstance(res, Awaitable) and not isinstance(res, Coroutine):
                    res = self.worker_for_awaitable_but_not_coro(res, job)

            if isinstance(res, Coroutine):
                self.daemonized_tasks.add(task := asyncio.create_task(res))
                job.running_task = task
            else:
                pass
                # TODO: Create warning message here
        else:
            self.sync_worker(job.task(), job)
            job.is_running = False

        return True

    @staticmethod
    async def worker_for_awaitable_but_not_coro(awaitable_but_not_coro: Awaitable, job: Job):
        job.is_running = True
        await awaitable_but_not_coro
        job.is_running = False
        job.running_task = None

    @staticmethod
    def sync_worker(target: Callable, job: Job):
        job.is_running = True
        target()
        job.is_running = False
