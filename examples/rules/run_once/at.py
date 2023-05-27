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


# Creating a datetime object denoting the current time + 10 seconds by hands
@scheduler.job(
    rule=RunOnce(at=datetime.now() + timedelta(seconds=10))
)
async def some_job():
    print('Executing some job..')


if __name__ == '__main__':
    asyncio.run(scheduler.run())
