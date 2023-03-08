import socketio
import asyncio

from src.namespaces import TaskNamespace, DataNamespace
from src.config import config


sio = socketio.AsyncClient()


async def main():
    sio.register_namespace(TaskNamespace("/task"))
    sio.register_namespace(DataNamespace("/data"))

    await sio.connect(
        "http://localhost:3002", 
        headers={
            "serverid": config["SERVER_ID"]
        },
        auth={ 
            config["AUTH_TOKEN_KEY"]: config["AUTH_TOKEN"] 
        }
    )
    await sio.wait()


if __name__ == "__main__":
    asyncio.run(main())
