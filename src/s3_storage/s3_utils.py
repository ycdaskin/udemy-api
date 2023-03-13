import uuid
import boto3
import os

AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")

def generate_secure_name(file):
    splitted = file.filename.split(".")
    extension = splitted[1] if len(splitted) > 1 else ""
    new_name = f'{str(uuid.uuid4())}-{str(uuid.uuid4())}'
    return f'{new_name}.{extension}'


def delete_file(key):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name="eu-central-1"
    )
    s3.delete_object(Bucket="beasy", Key=key)
