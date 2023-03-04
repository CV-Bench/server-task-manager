import boto3
import os

from src.config import config
from src.constants import Buckets, datatype_bucket_map

import logging

logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

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

    def upload_data(data, key):
        client = S3.create_s3_client()
        
        client.put_object(
            Bucket=config["BUCKET_NAME"],
            Key=key,
            Body=data
        )

    def get_object(key):
        client = S3.create_s3_client()

        return client.get_object(
            Bucket=config["BUCKET_NAME"],
            Key=key
        ).get("Body")

    def list_objects(prefix):
        client = S3.create_s3_client()

        return client.list_objects(
            Bucket=config["BUCKET_NAME"],
            Prefix=prefix
        )

    class Model:
        def get(id):
            return S3.get_object(
                os.path.join(Buckets.MODELS, id)
            )
        
        def list(prefix):
            return S3.list_objects(
                os.path.join(Buckets.MODELS, prefix)
            )
        
    class Background:
        def get(id):
            return S3.get_object(
                os.path.join(Buckets.BACKGROUNDS, id)
            )
        
        def list(prefix):
            return S3.list_objects(
                os.path.join(Buckets.BACKGROUNDS, prefix)
            )
        
    def build_key(data_type, id, extension):
        bucket = datatype_bucket_map(data_type)

        return os.path.join(bucket, id + "." + extension)