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
    rule=RunEvery(timedelta(seconds=10), repeat=3)
)
async def some_job():
    print('Executing some job..')


# Similar to simple, but scheduler will stop reschedule job every 10 seconds after 3 repeats.
# This job object will never execute again!
#
# Executing some job..  # Repeats: 1
# Executing some job..  # Repeats: 2
# Executing some job..  # Repeats: 3
#
# *nothing more*
#

if __name__ == '__main__':
    asyncio.run(scheduler.run())
