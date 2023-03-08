import socketio

from src.logger import logger

class LogNamespace(socketio.AsyncClientNamespace):
    background_tasks = set()

    def on_connect(self):
        logger.info("Namespace /log connected.")

    def on_disconnect(self):
        logger.warning("Namespace /log disconnected.")