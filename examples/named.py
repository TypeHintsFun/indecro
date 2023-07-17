import asyncio
from datetime import timedelta

from indecro import Scheduler
from indecro.executor import Executor
from indecro.storage.memory_storage import MemoryStorage
from indecro.rules import RunEvery

scheduler = Scheduler(
    executor=Executor(),
    storage=MemoryStorage()
)


async def foo(func_name: str):
    print(1)
    scheduler.remove_job(func_name)


async def main():
    scheduler.add_job(
        task=foo,
        rule=RunEvery(timedelta(seconds=1)),
        func_name="func_name"
    )
    await scheduler.run()


asyncio.run(main())
