import asyncio
from datetime import timedelta

from indecro import Scheduler
from indecro.executor import Executor
from indecro.rules import RunOnce
from indecro.storage.memory_storage import MemoryStorage

scheduler = Scheduler(
    executor=Executor(),
    storage=MemoryStorage()
)


@scheduler.job(
    rule=RunOnce(after=timedelta(seconds=10))
)
async def some_job():
    print('Executing some job..')


async def some_another_job():
    print('Executing some another job..')


scheduler.add_job(
    some_another_job,
    rule=RunOnce(after=timedelta(seconds=20))
)

if __name__ == '__main__':
    asyncio.run(scheduler.run())
