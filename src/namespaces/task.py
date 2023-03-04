from src.database import Database
import socketio
import asyncio
import traceback

from src.logger import logger
from src.config import config
from src.task import start_task, stop_task, cleanup_task
from src.constants import Socket

class TaskNamespace(socketio.AsyncClientNamespace):
    background_tasks = set()

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

    async def add_task(self, handler):
        task = asyncio.create_task(handler())

        self.background_tasks.add(task)

        task.add_done_callback(self.background_tasks.discard)

    async def on_start(self, data):
        await self.add_task(lambda: self.handle_on_start(data))

    async def on_stop(self, data):
        await self.add_task(lambda: self.handle_on_stop(data))

    async def on_cleanup(self, data):
        await self.add_task(lambda: self.handle_on_cleanup(data))