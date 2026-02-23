"""

Requirements:
- A lot of tasks keep comming
- Each task will have some priority
- We can implement different strtategy to pick a task from the q
- We will have x number of worker threads. (Initializer at the begining)
- Log for each task (Normal console logging). INFO (later we can expand)
- A strategy to rerun the failed task




Classes:

TaskAbstract - Done
    - Run task 1 time
    - run some cron job (can add some delay if sime job is already running)

PRIORITYENUM - Done
    - LOW
    - HIGH
- TaskPickStrategyAbstract
    - HigherPriorityFirst
    - INOrder - by timestamp

LogrocessorAbstract:
    - InfoLogProcessor

TaskSchedullerController

FailedTaskRerunStrategyAbstract
    - Increase the task priority and add to q
    - 

TaskQueue

"""

from __future__ import annotations
from abc import ABC, abstractmethod
import datetime
import time
from enum import Enum
import threading



class TaskPriority(Enum):
    LOW = 1
    HIGH = 2

class TaskAbstract(ABC):
    id: int
    timestamp: datetime.datetime
    priority: TaskPriority

    def __init__(self, id, timestamp: datetime.datetime, priority: TaskPriority):
        self.id = id
        self.timestamp = datetime.datetime.now()
        self.priority = priority

    @abstractmethod
    def run(self): pass

    def set_priority(self, priority: TaskPriority):
        self.priority = priority


class OnTimeTask(TaskAbstract):


    def run(self):
        time.sleep(3)



class CronJobTask(TaskAbstract):
    repeate_time: datetime.datetime

    def __init__(self, id, timestamp: datetime.datetime, priority: TaskPriority, repeate_time: datetime.datetime):
        self.repeate_time = repeate_time
        super().__init__(id, timestamp, priority)

    def run(self):
        time.sleep(3)


class TaskQueue:
    q: list[TaskAbstract]
    lock: threading.Lock
    condition:threading.Condition

    def __init__(self):
        self.q = []
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

    def remove(self, task):
        if task in self.q:
            self.q.remove(task)

        
    def find_by_priority(self, priority: TaskPriority):
        task_selected = None
        with self.condition:
            for task in self.q:
                if task.priority == priority:
                    task_selected = task
                    break
            if task_selected != None:
                self.remove(task_selected)
            self.condition.notify()
        return task_selected
    
    def add(self, task: TaskAbstract):
        with self.condition:
            self.q.append(task)
        
            self.condition.notify()



class TaskPickStrategyAbstract(ABC):

    @abstractmethod
    def pick_task(self, queue: TaskQueue): pass



class HigherPriorityFirst(TaskPickStrategyAbstract):

    def pick_task(self, queue: TaskQueue):
        high_priority_task = queue.find_by_priority(TaskPriority.HIGH)

        if high_priority_task != None: return high_priority_task

        return queue.find_by_priority(TaskPriority.LOW)


class LogTypeEnum(Enum):
    INFO = 1


class LogrocessorAbstract(ABC):

    next_processor: LogrocessorAbstract

    def __init__(self, next_processor: LogrocessorAbstract = None):
        self.next_processor = next_processor

    def log(self, type:LogTypeEnum, message: str):
        if self.next_processor != None:
            self.next_processor.log(type, message)


class InfoLogProcessor(LogrocessorAbstract):

    def log(self, type:LogTypeEnum, message: str):
        if type == LogTypeEnum.INFO:
            print(f"INFO: {message}")
        else:
            super().log(type, message)



class FailedTaskReRunStrategyAbstract(ABC):

    @abstractmethod
    def retry(self, q: TaskQueue, task: TaskAbstract): pass


class IncreasePriorityStrategy(FailedTaskReRunStrategyAbstract):

    def retry(self, q: TaskQueue, task: TaskAbstract):
        task.set_priority(TaskPriority.HIGH)
        q.add(task)



class Worker(threading.Thread):
    def __init__(self, id: int, task_queue: TaskQueue):
        super().__init__()
        self.task_queue = task_queue
        self.id = id
        self.task_pick_strategy = HigherPriorityFirst()
        self.failed_task_rerun_strategy = IncreasePriorityStrategy()
    
    def run(self):
        logger.log(LogTypeEnum.INFO, f"Worker {self.id} started.")
        while True:
            task = self.task_pick_strategy.pick_task(self.task_queue)
            if task is None: continue
            try:
                logger.log(LogTypeEnum.INFO, f"Worker {self.id} picked Task {task.id}")
                task.run()
            except Exception as e:
                logger.log(LogTypeEnum.INFO, f"Worker {self.id}: {e}")
                self.failed_task_rerun_strategy.retry(self.task_queue, task)
        


class TaskSchedullerController:
    task_queue: TaskQueue
    workers: list[Worker]
    worker_count: int

    def __init__(self, worker_count: int):
        self.worker_count = worker_count
        self.task_queue = TaskQueue()
        self.workers = [Worker(i+1, self.task_queue) for i in range(worker_count)]
        
    
    def add_task(self, task: TaskAbstract):
        self.task_queue.add(task)
    
    def start_workers(self):
        for worker in self.workers:
            worker.start()



    
    

    



# logger = InfoLogProcessor()
# task_controller = TaskSchedullerController(10)
# task_controller.start_workers()

import random

# Sample Task that fails randomly to test retry logic
class RandomFailTask(TaskAbstract):
    def run(self):
        time.sleep(1)
        if random.random() < 0.3:
            raise Exception("Random failure occurred")
        print(f"Task {self.id} completed successfully")


if __name__ == "__main__":
    logger = InfoLogProcessor()
    task_controller = TaskSchedullerController(worker_count=3)
    task_controller.start_workers()

    # Add 5 OnTimeTasks
    for i in range(5):
        task = OnTimeTask(id=i, timestamp=datetime.datetime.now(), priority=TaskPriority.LOW)
        task_controller.add_task(task)

    # Add 3 RandomFailTasks (to test retry)
    for i in range(5, 8):
        task = RandomFailTask(id=i, timestamp=datetime.datetime.now(), priority=TaskPriority.LOW)
        task_controller.add_task(task)

    # Add 2 CronJobTasks (note: they won't requeue unless you implement that)
    for i in range(8, 10):
        cron_task = CronJobTask(
            id=i,
            timestamp=datetime.datetime.now(),
            priority=TaskPriority.HIGH,
            repeate_time=datetime.datetime.now() + datetime.timedelta(seconds=5)
        )
        task_controller.add_task(cron_task)

    # Let the system run for a bit (simulate async processing)
    time.sleep(20)
    print("Main thread done. (Workers still running)")