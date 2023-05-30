import asyncio

from indecro import Scheduler
from indecro.executor import Executor
from indecro.rules import RunWhen
from indecro.storage.memory_storage import MemoryStorage

scheduler = Scheduler(
    executor=Executor(),
    storage=MemoryStorage()
)


def get_execute_flag():
    return input('Execute some job? y/[n] ').lower() in ('yes', 'y', '+')


# Job will be executed when provided callable's return will be truthy
#
# Execute some job? y/[n]
# *waiting 1 second*
# Execute some job? y/[n] n
# *waiting 1 second*
# Execute some job? y/[n] y
# *waiting 1 second*
# Executing some job..
# *waiting 1 second*
# Execute some job? y/[n] y
# Executing some job..
# *waiting 1 second*
# Execute some job? y/[n] no
#
# Provided callable must have not non-optional parameters

@scheduler.job(
    rule=RunWhen(get_execute_flag)
)
async def some_job():
    print('Executing some job..')


if __name__ == '__main__':
    asyncio.run(scheduler.run())
