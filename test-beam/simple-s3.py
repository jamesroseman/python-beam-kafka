import os
import posixpath

import apache_beam as beam
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions


def run():
    working_path = os.path.dirname(__file__)

    # Set environment variables.
    os.environ["AWS_ACCESS_KEY"] = "minioadmin"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "minioadmin"
    os.environ["AWS_REGION"] = "us-east-1"
    os.environ["S3_ENDPOINT"] = "http://localhost:9000"

    options = PipelineOptions([
        # "--runner=DirectRunner",
        # "--environment_type=LOOPBACK",
        "--runner=FlinkRunner",
        "--flink_version=1.16",
        "--flink_master=localhost:8081",
        "--environment_type=EXTERNAL",
        "--environment_config=localhost:50000",
        f"--setup_file={posixpath.join(working_path, 'setup.py')}",
        "--flink_submit_uber_jar",
        "--s3_region_name=us-east-1",
        "--s3_access_key_id=minioadmin",
        "--s3_secret_access_key=minioadmin",
        "--s3_endpoint=http://localhost:9000"
    ])

    with beam.Pipeline(options=options) as p:
        (p
            | 'Create words' >> beam.Create(['to be or not to be'])
            | 'Split words' >> beam.FlatMap(lambda words: words.split(' '))
            | 'Write to S3' >> WriteToText('s3://beam/simple-s3/output/output-file')
        )


if __name__ == "__main__":
    run()
