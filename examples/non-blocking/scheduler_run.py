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


async def my_loop():
    while True:
        print('Work in loop..')
        await asyncio.sleep(10)  # At least, write here await asyncio.sleep(0) to передать thread control


async def main():
    scheduler_task = asyncio.create_task(scheduler.run())
    my_loop_task = asyncio.create_task(my_loop())

    await asyncio.gather(scheduler_task, my_loop_task)

    # You also can execute your code while scheduler is running


asyncio.run(main())
