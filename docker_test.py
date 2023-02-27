import subprocess
import os
import docker
import time

def start_training(uid, ):
    pwd = os.getcwd()
    call = f"docker run -it --gpus all --memory 16g -v {pwd}/users/{uid}/dataset/:/data/input -v {pwd}/users/{uid}/training/:/data/output --name {uid}-training mmdetection:v0 configs/_user_/retinanet.py"
    subprocess.Popen(call.split(' '), )
    
def stop_training(uid):
    docker.from_env().containers.get(f"{uid}-training").stop()
    

start_training(uid = 19938882)

for i in range(10):
    print(docker.from_env().containers)
    time.sleep(1)

stop_training(uid = 19938882)