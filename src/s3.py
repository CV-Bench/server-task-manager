import boto3
import os

from src.config import config
from src.constants import Buckets


class S3:
    def create_s3_client():
        session = boto3.session.Session()

        return session.client(
            "s3", 
            endpoint_url=config["S3_ENDPOINT_URL"],
            region_name=config["S3_REGION"],
            aws_access_key_id=config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"]
        )


    # def upload_data(task_id, data, key):
    #     client = S3.create_s3_client()
        
    #     client.put_object(
    #         Bucket=config["BUCKET_NAME"],
    #         Key=task_id + "_" + key,
    #         Body=data,
    #         ACL='private',
    #     )


    # def delete_many(objects):
    #     client = S3.create_s3_client()

    #     client.delete_objects(
    #         Bucket=config["BUCKET_NAME"],
    #         Delete={
    #             "Objects": [
    #                 {
    #                     'Key': object
    #                 } for object in objects
    #             ]
    #         },
    #         RequestPayer='requester'
    #     )

    def get_object(key):
        client = S3.create_s3_client()

        return client.get_object(
            Bucket=config["BUCKET_NAME"],
            Key=key
        ).get("Body")


    class Model:
        def get(id):
            return S3.get_object(
                os.path.join(Buckets.MODELS, id)
            )
        
    class Background:
        def get(id):
            return S3.get_object(
                os.path.join(Buckets.BACKGROUNDS, id)
            )