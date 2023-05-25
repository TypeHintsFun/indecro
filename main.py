import asyncio
import time
from datetime import datetime, timedelta

from indecro.api.job import RunAs
from indecro.executor import Executor
from indecro.storage.memory_storage import MemoryStorage

from indecro.scheduler import Scheduler

from indecro.rules import SingleRun

scheduler = Scheduler(
    storage=MemoryStorage(),
    executor=Executor()
)


@scheduler.task(
    rule=SingleRun(when=datetime.now() + timedelta(seconds=10)),
    daemonize=RunAs.ASYNC_TASK
)
@scheduler.task(
    rule=SingleRun(when=datetime.now() + timedelta(seconds=10)),
    daemonize=RunAs.THREAD
)
async def one_minute():
    print('task started')
    await asyncio.sleep(10)
    print('task finished')


print('start time', datetime.now())

asyncio.run(scheduler.run())
