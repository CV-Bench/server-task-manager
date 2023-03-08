import os
import logging
import asyncio

from watchdog.events import FileSystemEventHandler, FileModifiedEvent

from src.constants import TaskType
from src.constants import Socket
from src.database import Database


logging.getLogger('watchdog').setLevel(logging.CRITICAL)
logging.getLogger('asyncio').setLevel(logging.CRITICAL)


class TaskLogUpdateHandler(FileSystemEventHandler):
    def __init__(self, task_namespace, task_id):
        super().__init__()

        self.task_namespace = task_namespace
        self.task_id = task_id

    def emit(self, data):
        asyncio.run(
            self.task_namespace.emit(
                Socket.LOG_UPDATE, 
                {
                    "data": data, 
                    "taskId": self.task_id,
                    "timestamp": Database.utc_now() 
                }
            )
        )


class DatasetLogWatcher(TaskLogUpdateHandler):
    def on_modified(self, event):
        if not isinstance(event, FileModifiedEvent):
            return

        with open(event.src_path, "r") as file:
            lines = file.readlines()

            lines = lines if len(lines) <= 100 else lines[:-100]

            self.emit(lines)


class NetworkLogWatcher(TaskLogUpdateHandler):
    def on_modified(self,  event):
        print(f'event type: {event.event_type} path : {event.src_path}')


task_log_watcher = {
    TaskType.CREATE_DATASET: DatasetLogWatcher,
    TaskType.CREATE_NETWORK: NetworkLogWatcher
}


get_watcher_path = lambda pwd, task_id, e: {
    TaskType.CREATE_DATASET: os.path.join(pwd, "data", "tasks", task_id, "log"),
    TaskType.CREATE_NETWORK: os.path.join(pwd, "data", "tasks", task_id, "log")
}[e]