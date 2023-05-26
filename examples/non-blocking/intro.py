import asyncio
import time
from datetime import timedelta

from indecro import Scheduler
from indecro.executor import Executor
from indecro.storage import MemoryStorage
from indecro.rules import RunOnce

scheduler = Scheduler(
    executor=Executor(),
    storage=MemoryStorage()
)


@scheduler.job(  # You also can schedule one function more than once
    rule=RunOnce(after=timedelta(seconds=10))
)
@scheduler.job(
    rule=RunOnce(after=timedelta(seconds=10))
)
def do_something():
    print('Starting task')
    time.sleep(10)
    print('Task finished')


# Jobs will be executed absolutely sequential because you dont provided any "parallel" executing method
# asynchronous functions doesnt help you because in this mode indecro will sequential execute async functions too
#
# *waiting 10 seconds*
# Starting task
# *waiting 10 seconds*
# Task finished
# *waiting 10 seconds*
# Starting task
# *waiting 10 seconds*
# Task finished

if __name__ == '__main__':
    asyncio.run(scheduler.run())
