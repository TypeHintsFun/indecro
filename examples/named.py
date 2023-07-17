import asyncio
from datetime import timedelta, datetime

from indecro import Scheduler
from indecro.executor import Executor
from indecro.job import Job
from indecro.storage.memory_storage import MemoryStorage
from indecro.rules import RunEvery, RunOnce

scheduler = Scheduler(
    executor=Executor(),
    storage=MemoryStorage()
)


async def foo(job_id: str):
    print(1)
    # Remove task by id
    scheduler.remove_job(job_id)


scheduler.add_job(
    task=foo,
    rule=RunEvery(timedelta(seconds=1)),
    id='job_id',  # Job id for indecro

    job_id='job_id'  # Same job id, that will be provided into task callable
)

scheduler.start()
