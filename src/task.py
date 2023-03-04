import os
import traceback
import shutil
import re

from src.constants import TaskType
from src.utils import Utils
from src.database import Database
from src.logger import logger
from src.config import config


## Format of all Database objects can be found in frontend repo in packages/shared-types


def start_training(id, task_data):
    # task_data = { datasetId, netowrkArchitectureId } ✔️

    ## Get the identifier of the network architecture (Use Database.get_network_architecture for this) ?
    
    ## Make sure the dataset is in the local file storage in /data/dataset/[datasetid] ✔️

    ## Start docker with key from network architecture object and dataset ✔️

    # Return true when everything worked, else return false ?
    
    
    
    config_lookup = {
        'retinanet_r50_fpn': 'configs/_user_/retinanet_r50_fpn.py',
        'faster_rcnn_r50_fpn': 'configs/_user_/faster_rcnn_r50_fpn.py',
    }
    
    # retrieve network architecture and dataset id
    network_architecture = task_data.get('networkArchitectureId') 
    dataset_id = task_data.get('datasetId')
    
    # check if both are specified
    if network_architecture is None:
        raise KeyError()(f'Task {id}: No network architecture specified in ')
    if dataset_id is None:
        raise KeyError()(f'Task {id}: No dataset id specified')
    
    # check if network architecture is supported
    if network_architecture not in config_lookup.keys():
        raise ValueError()(f'Task {id}: Network architecture {network_architecture} not supported')
    
    # Set Docker run command
    docker_command = 'docker run -it --gpus all --memory 16g'

    # Mount input and output folders
    pwd = os.getcwd()
    input_mount = f'-v {pwd}/data/dataset/{datasetid}:/data/input'
    output_mount = f'-v {pwd}/data/network/{id}:/data/output'

    # Set environment variables
    endpoint_env = f'-e ENDPOINT={config["HOST_DOMAIN"]}/task/'
    id_env = f'-e ID={id}'

    # Set Docker run name and image
    run_name = f'--name {id}'
    image = 'mmdetection'

    # Get neural network configuration from lookup table
    nn_config = config_lookup[network_architecture]

    # Build Docker run command
    call = f"{docker_command} {input_mount} {output_mount} {endpoint_env} {id_env} {run_name} {image} {nn_config}"

    Utils.Docker.stop_and_remove(id)
    Utils.Docker.start(call)
    
    return True ### THIS IS JUST A PLACEHOLDER, CHANGE THIS TO THE CORRECT RETURN VALUE WITH DOCKER API


def start_dataset_creation(id, task_data):
    pwd = os.getcwd()

    base_path = os.path.join(pwd, "data")

    Utils.Dataset.get_and_save_dataset_configuration(
        os.path.join(base_path, "tasks", str(id)), 
        task_data["datasetConfigurationId"]
    )

    # Download and save models and backgrounds

    model_paths = Utils.Dataset.get_and_save_models(
        os.path.join(base_path, "models"),
        task_data["modelIds"]
    )
    
    background_paths = Utils.Dataset.get_and_save_backgrounds(
        os.path.join(base_path, "backgrounds"),
        task_data["backgrounds"]
    )

    # Copy all Backgrounds

    backgrounds_base_path = os.path.join(base_path, "tasks", id, "backgrounds")

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

    # Start the Task

    Utils.Docker.stop_and_remove(id)

    startup_command = (
        f"docker run -d --memory 16g "
        f"-v {pwd}/data/tasks/{id}:/data/input "
        f"-v {pwd}/data/datasets/{id}:/data/output "
        f"-v {pwd}/data/tasks/{id}/config.json:/data/config/config.json "
        f"--name {id} blender-gen --taskID {id}"
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