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