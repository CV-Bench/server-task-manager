import subprocess
import os
import docker

from src.s3 import S3


def get_configuration(taskID: str) -> tuple[str, dict, str]:

    uid = 0
    configuration = {}
    flags = ""

    return uid, configuration, flags  # TODO


def make_filesystem(taskID: str, uid: str, dataset_configuration: dict) -> dict:

    for path in ["bg/static", "bg/dynamic", "config", "models", "textures"]:
        os.makedirs(os.path.join(f"users/{uid}/dataset.{taskID}/", path))

    for i, obj_id in enumerate(dataset_configuration["input"]["object"]):
        obj = S3.Model.get(obj_id)

        with open(f"users/{uid}/dataset.{taskID}/models/{obj_id}", "w") as f:
            f.write(obj)

        dataset_configuration["input"]["object"][i] = dict(
            model=obj_id,
            texture=None,
            label=obj["modelObject"]["filename"]
        )

    for i, obj_id in enumerate(dataset_configuration["input"]["distractor"]):
        obj = S3.Model.get(obj_id)
        with open(f"users/{uid}/dataset.{taskID}/models/{obj_id}", "w") as f:
            f.write(obj)

        dataset_configuration["input"]["distractor"][i] = dict(
            model=obj_id,
            texture=None,
        )

    for i, bg_id in enumerate(dataset_configuration["input"]["bg"]):
        bg = S3.Background.get(bg_id)
        with open(f"users/{uid}/dataset.{taskID}/bg/static/{obj_id}", "w") as f:
            f.write(bg)

    with open(f"users/{uid}/dataset.{taskID}/config/config.json", "w") as f:
        f.write(dataset_configuration)

    return dataset_configuration


def start(taskID: str) -> None:

    uid, dataset_configuration, flags = get_configuration(taskID)

    dataset_configuration = make_filesystem(taskID, uid, dataset_configuration)

    pwd = os.getcwd()
    call = f"docker run --rm --gpus all --memory 16g -v {pwd}/users/{uid}/dataset.{taskID}/:/data/input -v {pwd}/users/{uid}/training/:/data/output --name {uid}-training blender-gen --taskID {uid} {flags}"
    subprocess.Popen(call.split(' '), )


def stop(taskID: str) -> None:

    uid = get_configuration(taskID)[0]

    docker.from_env().containers.get(f"{uid}-dataset").stop()


def cleanup(taskID: str) -> None:

    uid = get_configuration(taskID)[0]

    os.rmdir(f"users/{uid}/dataset.{taskID}/")
