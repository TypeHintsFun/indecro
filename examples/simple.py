import asyncio
from datetime import datetime, timedelta

from indecro import Scheduler
from indecro.executor import Executor
from indecro.rules import RunOnce
from indecro.storage.memory_storage import MemoryStorage

scheduler = Scheduler(
    executor=Executor(),
    storage=MemoryStorage()
)


@scheduler.job(
    rule=RunOnce(at=datetime.now() + timedelta(seconds=10))
)
async def some_job():
    print('Executing some job..')


async def some_another_job():
    print('Executing some another job..')


scheduler.add_job(
    some_another_job,
    rule=RunOnce(at=datetime.now() + timedelta(seconds=20))
)


asyncio.run(scheduler.run())
