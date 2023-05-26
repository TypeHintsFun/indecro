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
    rule=RunEvery(timedelta(seconds=10), after=timedelta(seconds=20))
)
async def some_job():
    print('Executing some job..')


# Similar to simple, but scheduler will start execute job every 10 seconds only after an 20 seconds delay
#
# *waiting 20 seconds*
# Executing some job..
# *waiting 10 seconds*
# Executing some job..
# *waiting 10 seconds*
# Executing some job..
# *waiting 10 seconds*
# Executing some job..
# *waiting 10 seconds*
# Executing some job..
# ...

if __name__ == '__main__':
    asyncio.run(scheduler.run())
