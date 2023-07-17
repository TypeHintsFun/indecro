from datetime import timedelta

from indecro import Scheduler
from indecro.executor import Executor
from indecro.rules import RunEvery
from indecro.storage.memory_storage import MemoryStorage

scheduler = Scheduler(
    executor=Executor(),
    storage=MemoryStorage()
)


async def foo(job_id: str):
    print(1)
    # DO NOT USE THIS IN REAL TASKS! Use RunOnce instead
    # Remove task by id
    scheduler.remove_job(job_id)


scheduler.add_job(
    task=foo,
    rule=RunEvery(timedelta(seconds=1)),
    id='job_id',  # Job id for indecro

    job_id='job_id'  # Same job id, that will be provided into task callable
)

scheduler.start()
