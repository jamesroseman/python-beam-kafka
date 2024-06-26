import os
import subprocess
from setuptools import setup, find_packages, Command

import boto3


# Your S3 bucket details
S3_BUCKET = 'beam'
S3_TEMP_LOCATION = 's3://tmp/'

# Define your package details
PACKAGE_NAME = 'test_beam_pipelines'
PACKAGE_VERSION = '0.0.1'
DESCRIPTION = 'Test Beam pipelines.'
REQUIREMENTS = [
    'apache-beam',
    'boto3',  # Add boto3 to your requirements
]


class UploadToS3Command(Command):
    description = 'Build and upload the package to S3'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # Build the distribution
        self.run_command('sdist')

        # Upload the distribution to S3
        dist_file = f'dist/{PACKAGE_NAME}-{PACKAGE_VERSION}.tar.gz'
        s3_key = os.path.join('temp', f'{PACKAGE_NAME}-{PACKAGE_VERSION}.tar.gz')
        s3 = boto3.client('s3')

        if os.path.exists(dist_file):
            s3.upload_file(dist_file, S3_BUCKET, s3_key)
            print(f'Uploaded {dist_file} to s3://{S3_BUCKET}/{s3_key}')
        else:
            print(f"Error: {dist_file} does not exist. Make sure the package has been built before uploading.")


# Standard setup
setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    cmdclass={
        'upload_to_s3': UploadToS3Command,
    },
)
