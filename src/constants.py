class TaskStatus:
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    ABORTED = "ABORTED"
    FINISHED = "FINISHED"


class TaskType:  
    CREATE_NETWORK = "CREATE_NETWORK"
    CREATE_DATASET = "CREATE_DATASET"


class Buckets:
    MODELS = "models"
    DATASETS = "datasets"
    BACKGROUNDS = "backgrounds"
    NETWORKS = "networks"


class DataType:
    MODEL = "MODEL",
    DATASET = "DATASET"
    NETWORK = "NETWORK"


datatype_path_map = lambda e: {
    DataType.DATASET: "datasets",
    DataType.NETWORK: "networks"
}[e]


datatype_bucket_map = lambda e: {
    DataType.DATASET: Buckets.DATASETS,
    DataType.NETWORK: Buckets.NETWORKS
}[e]


class Socket:
    DATA_UPLOADED = "data_uploaded"
    UPLOAD_FAILED = "upload_failed"
    DATA_DELETED = "data_deleted"

    TASK_STOPPED = "task_stopped"
    STOP_FAILED = "stop_failed"
    TASK_CLEANED = "task_cleaned"
    CLEANUP_FAILED = "cleanup_failed"
    TASK_STARTED = "task_started"
    START_FAILED = "start_failed"