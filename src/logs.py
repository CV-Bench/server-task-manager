import os
import logging
import asyncio

from watchdog.events import FileSystemEventHandler, FileModifiedEvent

from src.constants import TaskType
from src.constants import Socket, Logs
from src.database import Database
from src.config import config


logging.getLogger('watchdog').setLevel(logging.CRITICAL)
logging.getLogger('asyncio').setLevel(logging.CRITICAL)


class TaskLogUpdateHandler(FileSystemEventHandler):
    def __init__(self, task_namespace, task_id, queue):
        super().__init__()

        self.task_namespace = task_namespace
        self.task_id = task_id
        self.queue = queue

    def emit(self, data):
        self.queue.put_nowait(
            {
                "data": data, 
                "taskId": self.task_id,
                "timestamp": Database.utc_now().timestamp(),
                "serverId": config["SERVER_ID"]
            }
        )


class DatasetLogWatcher(TaskLogUpdateHandler):
    def __init__(self, *args, watch_path="", **kwargs):
        super().__init__(*args, **kwargs)

        stdout_path = os.path.join(watch_path, "stdout.txt")

        if os.path.exists(stdout_path):
            self.on_modified(FileModifiedEvent(stdout_path))

    def on_modified(self, event):
        if not isinstance(event, FileModifiedEvent):
            return

        with open(event.src_path, "r") as file:
            lines = file.readlines()

            lines = lines if len(lines) <= Logs.DATASET_MAX_LINES else lines[len(lines) - Logs.DATASET_MAX_LINES:]

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