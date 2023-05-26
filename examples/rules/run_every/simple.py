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
    rule=RunEvery(timedelta(seconds=10))
)
async def some_job():
    print('Executing some job..')


# some_job will be executed every 10 seconds ever, before you stop program or use scheduler.stop()
#
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
