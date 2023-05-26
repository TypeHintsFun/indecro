import asyncio
from datetime import timedelta

from indecro import Scheduler
from indecro.executor import Executor
from indecro.rules import RunEvery
from indecro.storage.memory_storage import MemoryStorage

scheduler = Scheduler(
    executor=Executor(),
    storage=MemoryStorage()
)


@scheduler.job(
    rule=RunEvery(timedelta(seconds=10), before=timedelta(seconds=25))
)
async def some_job():
    print('Executing some job..')


# Similar to simple, but scheduler will stop reschedule job every 10 seconds after 25 seconds.
# This job object will never execute again!
#
# Executing some job..
# Executing some job..
#
# *nothing more*
#

if __name__ == '__main__':
    asyncio.run(scheduler.run())
