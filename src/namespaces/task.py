from src.database import Database
import socketio
import asyncio
import traceback
import os

from watchdog.observers import Observer

from src.logger import logger
from src.config import config
from src.task import start_task, stop_task, cleanup_task
from src.constants import Socket
from src.utils import Utils
from src.logs import task_log_watcher, get_watcher_path


class TaskNamespace(socketio.AsyncClientNamespace):
    background_tasks = set()
    observers = {}
    task_queue = asyncio.Queue()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_task(self.handle_send_log_update)

    def on_connect(self):
        logger.info("Namespace /task connected.")

    def on_disconnect(self):
        logger.warning("Namespace /task disconnected.")

    async def handle_on_start(self, data):
        task_id = data["taskId"]

        logger.info(f"Start task {task_id}")

        task = Database.get_task(data["taskId"])

        task_type = task["type"]

        task_data = task["info"]

        is_success = start_task(task_id, task_type, task_data)

        await self.on_subscribe_task_log({ "taskId": task_id, "taskType": task_type})

        await self.emit(
            Socket.TASK_STARTED if is_success else Socket.START_FAILED, 
            {
                **data, "serverId": config["SERVER_ID"],
            }
        )

    async def handle_on_stop(self, data):
        task_id = data["taskId"] 

        logger.info(f"Stop task {task_id}")

        is_success =  stop_task(task_id)

        await self.emit(
            Socket.TASK_STOPPED if is_success else Socket.STOP_FAILED,
            {
                **data, "serverId": config["SERVER_ID"],
            }
        )

    async def handle_on_cleanup(self, data):
        task_id = data["taskId"] 

        logger.info(f"Cleanup task {task_id}")

        is_success = False

        try:
            is_success = cleanup_task(task_id)
        except:
            traceback.print_exc()

        await self.emit(
            Socket.TASK_CLEANED if is_success else Socket.CLEANUP_FAILED,
            {
                **data, "serverId": config["SERVER_ID"],
            }
        )

    async def handle_send_log_update(self):
        while True:
            if not self.task_queue.empty():
                while not self.task_queue.empty():

                    data = self.task_queue.get_nowait()

                    if data:
                        await self.emit(Socket.LOG_UPDATE, data)

            await asyncio.sleep(2)

    def add_task(self, handler):
        task = asyncio.create_task(handler())

        self.background_tasks.add(task)

        task.add_done_callback(self.background_tasks.discard)

    async def on_start(self, data):
        await self.add_task(lambda: self.handle_on_start(data))

    async def on_stop(self, data):
        await self.add_task(lambda: self.handle_on_stop(data))

    async def on_cleanup(self, data):
        await self.add_task(lambda: self.handle_on_cleanup(data))

    async def on_subscribe_task_log(self, data):
        task_id = data["taskId"]
        task_type = data["taskType"]

        if self.observers.get(task_id):
            return

        handler = task_log_watcher[task_type]

        if not handler:
            return
        
        logger.debug(f"Subscribe task log: {task_id}")
        
        watch_path = get_watcher_path(os.getcwd(), task_id, task_type)

        Utils.make_dir(watch_path)

        new_observer = Observer()
        new_observer.schedule(handler(self, task_id, self.task_queue, watch_path=watch_path), path=watch_path)
        new_observer.start()

        self.observers[task_id] = new_observer

    async def on_unsubscribe_task_log(self, data):
        task_id = data["taskId"]

        if not self.observers.get(task_id):
            return
        
        logger.debug(f"Unaubscribe task log: {task_id}")

        self.observers[task_id].stop()
        self.observers.pop(task_id)