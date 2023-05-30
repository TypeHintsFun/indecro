import asyncio

from indecro import Scheduler
from indecro.executor import Executor
from indecro.rules import RunWhen
from indecro.storage.memory_storage import MemoryStorage

# New imports. That's a kind of Magic!
from magic_filter import F

scheduler = Scheduler(
    executor=Executor(),
    storage=MemoryStorage()
)


class InputUser:
    @property
    def name(self):
        return input('Pls enter your name: ')


# Job will be executed when provided magic filter will be resolve subject.
#
#
# Pls enter your name: Bob
# *waiting 1 second*
# Pls enter your name: Daniel
# *waiting 1 second*
# Pls enter your name: Michael
# Executing some job..
# *waiting 1 second*
# Pls enter your name: Leonid
# *waiting 1 second*
# Pls enter your name:

user = InputUser()


@scheduler.job(
    rule=RunWhen(subject=user, will=F.name.lower() == 'michael')
)
async def some_job():
    print('Executing some job..')


if __name__ == '__main__':
    asyncio.run(scheduler.run())
