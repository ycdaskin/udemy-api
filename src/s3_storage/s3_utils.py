import uuid
import boto3


def generate_secure_name(file):
    splitted = file.filename.split(".")
    extension = splitted[1] if len(splitted) > 1 else ""
    new_name = f'{str(uuid.uuid4())}-{str(uuid.uuid4())}'
    return f'{new_name}.{extension}'


def delete_file(key):
    s3 = boto3.client(
        "s3",
        aws_access_key_id="AKIA5CHGUKFPBI5XIJOX",
        aws_secret_access_key="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",
        region_name="eu-central-1"
    )
    s3.delete_object(Bucket="beasy", Key=key)
