# from flask import Flask

# app = Flask(__name__)

# @app.route("/generate")
# def generate_blender():


# @app.route("/train")
# def hello_world():
#     return "<p>Hello, World!</p>"

import docker
import os
from flask import Flask

app = Flask(__name__)

@app.route("/train")
def train():
    gpu = docker.types.DeviceRequest(device_ids=["0"], capabilities=[['gpu']])
    pwd = os.getcwd()
    mounts = {
        os.path.join(pwd, "users/19938882/dataset"): {
            'bind': '/data/input',
            'mode': 'rw'
        },
        os.path.join(pwd, "users/19938882/training"): {
            'bind': '/data/output',
            'mode': 'rw',
        }
    }
    container = docker.from_env().containers.run(
        "mmdetection:v0", 
        device_requests=[gpu],
        volumes=mounts,
    ) 
    print(container)
    return "Training started"