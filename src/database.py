from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timezone

from src.config import config
from src.constants import TaskStatus


client = MongoClient(config.get("DB_HOST"))

db = client.cvBench


class Database:
    ## NETWORK ARCHITECTURE

    def get_network_architecture(networkArchitectureId):
        return db.networkArchitectures.find_one({
            "_id": ObjectId(networkArchitectureId)
        })

    ## DATASET CONFIGURATION

    def get_dataset_configuration(datasetConfigId):
        return db.datasetConfigurations.find_one({
            "_id": ObjectId(datasetConfigId)
        })
    
    ## MODELS

    def get_model_list(modelIds):
        return db.models.find({
            "_id": {
                "$in": [ObjectId(i) for i in modelIds]
            }
        })
    
    ## TASK

    def update_task(task_id, update):
        db.tasks.update_one({
            "_id": ObjectId(task_id)
        }, {
            "$set": {
                **update,
                "updatedAt": Database.utc_now()
            }
        })

    def get_task(task_id):
        return db.tasks.find_one({
            "_id": ObjectId(task_id)
        })

    def start_task(task_id, additional_args):
        db.tasks.update_one({
            "_id": ObjectId(task_id)
        }, {
            "$set": {
                **additional_args,
                "updatedAt": Database.utc_now(),
                "status": TaskStatus.RUNNING
            }
        })

    def utc_now():
        return datetime.now(timezone.utc)