import boto3
from botocore.exceptions import ClientError
from django.conf import settings


menu = [
    {'title': 'About us', 'url': 'about_us'},
    {'title': 'Contact us', 'url': 'contact_us'},
]


def ensure_bucket():
    s3 = boto3.client(
        's3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    try:
        s3.head_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            s3.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        else:
            raise