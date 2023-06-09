import asyncio
import time
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
    daemonize=RunAs.THREAD  # thread-based job demonizing
)
@scheduler.job(
    rule=RunOnce(after=timedelta(seconds=10)),
    daemonize=RunAs.THREAD
)
def do_something():
    print('Starting task')
    time.sleep(10)
    print('Task finished')


# TODO: Add thread-based "parallel" executing for async jobs

# For safety use of thread-based "parallel" jobs executing your jobs must be sync and thread-safe
#
# *waiting 10 seconds*
# Starting task
# Starting task
# *waiting 10 seconds*
# Task finished
# Task finished

if __name__ == '__main__':
    asyncio.run(scheduler.run())
