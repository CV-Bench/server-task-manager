import os
import traceback
import shutil
import re

from src.constants import TaskType
from src.utils import Utils
from src.database import Database
from src.logger import logger
from src.config import config
from src.constants import allowed_training_architecture_keys, Docker


## Format of all Database objects can be found in frontend repo in packages/shared-types


def start_training(id, task_data):
    network_architecture_id = task_data['networkArchitectureId'] 
    dataset_id = task_data['datasetId']

    network_architecture = Database.get_network_architecture(network_architecture_id)

    nn_identifier = network_architecture["identifier"]

    if not nn_identifier in allowed_training_architecture_keys:
        logger.error(f"[START TRAINING] Key {nn_identifier} not allowed.")

        return False
    
    pwd = os.getcwd()
    dataset_path = os.path.join(pwd, "data", "dataset", dataset_id)

    if not os.path.exists(dataset_path):
        logger.error(f"[START TASK] Dataset with ID {dataset_id} doesn't exist.")

        return False

    startup_command = (
        f"docker run -it --gpus all --memory 16g "
        # Volumes
        f"-v {pwd}/data/dataset/{dataset_id}:/data/input "
        f"-v {pwd}/data/network/{id}:/data/output "
        # Env variables
        f"-e ENDPOINT={config['HOST_DOMAIN']}/task/ "
        f"-e ID={id} "
        # Name
        f"--name {id} {Docker.OPENMM} configs/_user_/{nn_identifier}.py"
    )

    Utils.Docker.stop_and_remove(id)
    Utils.Docker.start(startup_command)
    
    return True


def start_dataset_creation(id, task_data):
    pwd = os.getcwd()

    base_path = os.path.join(pwd, "data")

    # Download and save models and backgrounds

    model_paths = Utils.Dataset.get_and_save_models(
        os.path.join(base_path, "models"),
        task_data["modelIds"]
    )
    
    background_paths = Utils.Dataset.get_and_save_backgrounds(
        os.path.join(base_path, "backgrounds"),
        task_data["backgroundIds"]
    )

    # Copy all Backgrounds

    backgrounds_base_path = os.path.join(base_path, "tasks", id, "backgrounds", "static")

    Utils.make_dir(backgrounds_base_path)

    for path in background_paths:
        key = path.split("/")[-1]

        shutil.copy(path, os.path.join(backgrounds_base_path, key))

    # Copy all Models

    model_base_path = os.path.join(base_path, "tasks", id, "models")

    for path in model_paths:
        key = path.split("/")[-1]

        model_path = os.path.join(model_base_path, key)

        Utils.make_dir(model_path)

        Utils.copy_dir(path, model_path)

    # Create config object

    Utils.Dataset.get_and_save_dataset_configuration(
        os.path.join(base_path, "tasks", str(id)), 
        task_data["configurationId"],
        task_data["modelIds"]
    )

    # Start the Task

    Utils.Docker.stop_and_remove(id)

    startup_command = (
        f"docker run -d --memory 16g "
        # Volumes
        f"-v {pwd}/data/tasks/{id}:/data/input "
        f"-v {pwd}/data/datasets/{id}:/data/output "
        f"-v {pwd}/data/tasks/{id}/config.json:/data/input/config/config.json "
        # Name
        f"--name {id} {Docker.BLENDER_GEN} "
        # Arguments
        f"--taskID {id} --endpoint {config['HOST_DOMAIN']}"
    )

    Utils.Docker.start(startup_command)

    logger.info(f"[DATASET CREATION] Starting {id}")

    return True


def start_task(task_id, task_type, task_data):
    # TODO Check how many containers are currently running and
    # return false when max is reached 

    PROCESS_TASK = {
        TaskType.CREATE_DATASET: start_dataset_creation,
        TaskType.CREATE_NETWORK: start_training
    }

    if not task_type in PROCESS_TASK.keys():
        return False

    try:
        return PROCESS_TASK[task_type](task_id, task_data)
    except:
        traceback.print_exc()
        return False


def stop_task(task_id):
    return Utils.Docker.stop_and_remove(task_id)


def cleanup_task(task_id):
    keep_files = re.compile("(output|log)\.(txt|json)")

    base_path = os.path.join(os.getcwd(), "data", "tasks", task_id)

    for path in os.listdir(base_path):
        if keep_files.search(path):
            continue

        path = os.path.join(base_path, path)

        Utils.rm_path(path)

    return True