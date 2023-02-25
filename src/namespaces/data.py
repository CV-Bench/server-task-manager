import socketio
from src.logger import logger


class DataNamespace(socketio.AsyncClientNamespace):
    def on_connect(self):
        logger.info("Namespace /data connected.")

        pass

    def on_disconnect(self):
        pass

    async def on_delete(self, data):
        pass

    async def on_upload(self, data):
        pass