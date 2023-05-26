import asyncio
from datetime import timedelta

from indecro.api.job import RunAs

from indecro import Scheduler
from indecro.executor import Executor
from indecro.storage import MemoryStorage
from indecro.rules import RunOnce

scheduler = Scheduler(
    executor=Executor(),
    storage=MemoryStorage()
)


@scheduler.job(
    rule=RunOnce(after=timedelta(seconds=10)),
    daemonize=RunAs.ASYNC_TASK  # async-based job demonizing
)
@scheduler.job(
    rule=RunOnce(after=timedelta(seconds=10)),
    daemonize=RunAs.ASYNC_TASK
)
async def do_something():
    print('Starting task')
    await asyncio.sleep(10)
    print('Task finished')


# To use async-based "parallel" jobs executing your jobs must also be asynchronous
#
# *waiting 10 seconds*
# Starting task
# Starting task
# *waiting 10 seconds*
# Task finished
# Task finished

if __name__ == '__main__':
    asyncio.run(scheduler.run())
