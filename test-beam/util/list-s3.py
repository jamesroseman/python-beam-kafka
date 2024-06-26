import boto3
from botocore.client import Config


def main():
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

    # List all buckets
    buckets = s3_client.list_buckets()

    # Iterate through each bucket and list all files
    for bucket in buckets['Buckets']:
        print(f"Bucket: {bucket['Name']}")
        objects = s3_client.list_objects_v2(Bucket=bucket['Name'])

        if 'Contents' in objects:
            for obj in objects['Contents']:
                print(f" - {obj['Key']}")
        else:
            print(" - No objects found")


if __name__ == "__main__":
    main()
