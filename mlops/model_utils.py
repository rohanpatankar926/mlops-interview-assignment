import boto3
from datetime import datetime
import os
#for saving space and cost in s3 also consider storing top 5 trained models for future references

def upload_model_to_s3(s3_bucket, model_path):
    model_name="final-model"
    model_version = datetime.now().strftime("%Y%m%d%H%M%S")
    s3_path = f"models/{model_name}_v{model_version}.pt"
    local_model_path = f"{model_path}/{model_name}.pt"
    s3_client = boto3.client('s3',aws_access_key=os.getenv("AWS_S3_ACCESS"),aws_secret_key=os.getenv("AWS_SECRET_KEY"))
    s3_client.upload_file(local_model_path, s3_bucket, s3_path)
    return model_version