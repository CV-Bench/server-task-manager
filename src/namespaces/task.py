import socketio
from src.logger import logger


class TaskNamespace(socketio.AsyncClientNamespace):
    def on_connect(self):
        logger.info("Namespace /task connected.")
        pass

    def on_disconnect(self):
        logger.warning("Namespace /task disconnected.")

        pass

    async def on_start(self, data):
        print("ON START", data)

        await self.emit("test", data)
        pass

    async def on_stop(self, data):
        print("ON STOP", data)

        pass