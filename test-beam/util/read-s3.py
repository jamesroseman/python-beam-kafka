import boto3
import sys
from botocore.client import Config
import os


def print_s3_file(bucket_name, file_path):
    # S3 connection details
    s3_endpoint_url = "http://localhost:9000"
    aws_access_key_id = "minioadmin"
    aws_secret_access_key = "minioadmin"
    region_name = "us-east-1"

    # Initialize S3 client
    s3_client = boto3.client(
        's3',
        endpoint_url=s3_endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
        config=Config(signature_version='s3v4')
    )

    try:
        # Get the object from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=file_path)
        content = response['Body'].read().decode('utf-8')
        print(content)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python read-s3.py <bucket> <path/to/file>")
        sys.exit(1)

    bucket_name = sys.argv[1]
    file_path = sys.argv[2]

    print_s3_file(bucket_name, file_path)