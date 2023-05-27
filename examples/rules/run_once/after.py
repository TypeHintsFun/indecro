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


# Similar, but using shortcut
@scheduler.job(
    rule=RunOnce(after=timedelta(seconds=10))
)
async def some_job():
    print('Executing some job..')


if __name__ == '__main__':
    asyncio.run(scheduler.run())
