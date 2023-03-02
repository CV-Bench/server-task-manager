from database import Database
import socketio

from src.logger import logger
from src.config import config
from src.task import start_task

class TaskNamespace(socketio.AsyncClientNamespace):
    def on_connect(self):
        logger.info("Namespace /task connected.")
        pass

    def on_disconnect(self):
        logger.warning("Namespace /task disconnected.")

        pass

    async def handle_on_start(self, data):
        task_id = data["taskId"]

        task = Database.get_task(data["taskId"])

        task_type = task["type"]

        task_data = task["info"]

        is_success = await start_task(task_id, task_type, task_data)

        ## TODO if success set task to running

        await self.emit(
            "task_started" if is_success else "start_failed", 
            {
                **data, "socketId": config["SERVER_ID"],
            }
        )

    async def on_start(self, data):
        self.handle_on_start(data)

    async def on_stop(self, data):
        print("ON STOP", data)

        pass