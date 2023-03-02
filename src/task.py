from src.constants import TaskType

## Format of all Database objects can be found in frontend repo in packages/shared-types


def start_training(id, task_data):
    # task_data = { datasetId, netowrkArchitectureId } 

    ## Get the identifier of the network architecture (Use Database.get_network_architecture for this)
    
    ## Make sure the dataset is in the local file storage in /data/dataset/[datasetid]

    ## Start docker with key from network architecture object and dataset

    # Return true when everything worked, else return false

    pass


def start_dataset_creation(id, task_data):
    # task_data = { modelId: str, backgrounds: [str], datasetConfigurationId: [id] }

    ## Check if Model and Background are already on the local file storage
    # If not, download them from s3 (Use S3.Background.get or S3.Model.get)
    # If so, do nothing

    # Get the dataset configuration and store it in appropriate format in /data/task/[id]
    # for usage in blender script (Use Database.get_dataset_configuratio for this)

    # in /data/task/[id] create appropriate folders and copy necessary models and backgrounds
    # into the folders

    # Start the docker with appropriate volumes and let the dataset be created in 
    # /data/dataset/[task_id]

    # Return true when everything worked, else return false

    pass


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
        return False
    

def stop_task(task_id):
    # TODO Stop task here, return false when stop failed, else return true
    pass