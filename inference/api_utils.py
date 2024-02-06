import boto3
import os
s3_client = boto3.client('s3',aws_access_key=os.getenv("AWS_S3_ACCESS"),aws_secret_key=os.getenv("AWS_SECRET_KEY"))

def get_latest_model_version_from_s3(s3_bucket, model_name):
    response = s3_client.list_objects_v2(Bucket=s3_bucket, Prefix=f"models/{model_name}_")
    objects = response.get('Contents', [])
    version_numbers = [int(obj['Key'].split(f"{model_name}_v")[1].split('.')[0]) for obj in objects]
    latest_version = max(version_numbers, default=None)
    return latest_version

def download_model_from_s3(s3_bucket, s3_path, local_model_path):
    s3_client.download_file(s3_bucket, s3_path, local_model_path)
