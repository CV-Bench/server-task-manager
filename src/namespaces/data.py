import socketio
import os
import asyncio
import traceback

from src.logger import logger
from src.config import config
from src.constants import datatype_path_map, Socket
from src.utils import Utils
from src.s3 import S3

class DataNamespace(socketio.AsyncClientNamespace):
    background_tasks = set()

    def on_connect(self):
        logger.info("Namespace /data connected.")

    def on_disconnect(self):
        logger.warning("Namespace /data disconnected.")

    async def on_delete(self, data):
        data_id = data["dataId"]
        data_type = data["dataType"]

        datatype_path = datatype_path_map(data_type)

        path = os.path.join(os.getcwd(), "data", datatype_path, data_id)

        Utils.rm_path(path)

        self.emit(Socket.DATA_DELETED, {
            **data,
            "serverId": config["SERVER_ID"]
        })

    async def handle_upload(self, data):
        data_id = data["dataId"]
        data_type = data["dataType"]

        datatype_path = datatype_path_map(data_type)

        path = os.path.join(os.getcwd(), "data", datatype_path, data_id)

        file_content = Utils.Upload.get_dir_as_zip(path)

        key = S3.build_key(data_type, data_id, "zip")

        is_success = True

        try: 
            S3.upload_data(file_content, key)

            logger.info(f"Data for {data_type} {data_id} uploaded.")
        except:
            traceback.print_exc()

            logger.error(f"Upload for {data_type} {data_id} failed.")
            
            is_success = False

        await self.emit(
            Socket.DATA_UPLOADED if is_success else Socket.UPLOAD_FAILED,
            {
                **data,
                "serverId": config["SERVER_ID"]
            }
        )

    async def on_upload(self, data):
        task = asyncio.create_task(self.handle_upload(data))

        self.background_tasks.add(task)

        task.add_done_callback(self.background_tasks.discard)