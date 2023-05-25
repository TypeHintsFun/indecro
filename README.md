### Intro 
Indecro is a small framework for task scheduling

All parts are designed to be replaceable. 

Main ideas are:
* No pickle! Tasks are stored in readable format, so can be used outside of framework
* Task creator doesn't need to know how tasks are implemented or executed
* Persistence may be implemented
* All workers must follow same async style: be either sync or async functions

Currently project is in the design stage and any APIs are to be changed

### How to use:

Create scheduler

```python
from indecro import Scheduler
from indecro.executor import Executor
from indecro.storage.memory_storage import MemoryStorage

scheduler = Scheduler(
    executor=Executor(),
    storage=MemoryStorage()
)
```

Schedule job using decorator-based shortcut (custom job name can be provided for compatibility)

```python
from datetime import datetime, timedelta

from indecro.rules import RunOnce
# Rule, theft control time when scheduled task would be executed


@scheduler.job(rule=RunOnce(at=datetime.now() + timedelta(seconds=10)))
async def some_job():
    print('Executing some job..')
```

Schedule job using direct function

```python
async def some_another_job():
    print('Executing some another job..')


scheduler.add_job(
    some_another_job,
    rule=RunOnce(at=datetime.now() + timedelta(seconds=20))
)
```

Run scheduler:

```python
await scheduler.run()
```