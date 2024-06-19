import json
import os
import posixpath

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.kafka import ReadFromKafka, WriteToKafka, default_io_expansion_service


class AddReadField(beam.DoFn):
    def process(self, element):
        # Decode the Kafka message (key, value)
        key, value = element
        # Parse the JSON value
        message = json.loads(value.decode('utf-8'))
        # Add the "read" field
        message['read'] = True
        # Convert back to JSON string
        updated_value = json.dumps(message).encode('utf-8')
        # Return the new key-value pair
        yield (key, updated_value)


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
        "--streaming",
        "--staging_location=s3://beam/staging",
        "--temp_location=s3://beam/temp",
    ])

    kafka_config = {
        "bootstrap.servers":"localhost:29092",
        "group.id": "simple-kafka-beam",
    }

    with beam.Pipeline(options=options) as pipeline:
        (pipeline
         | 'ReadFromKafka' >> ReadFromKafka(
             consumer_config=kafka_config,
             topics=['test-input-beam'],
             expansion_service=default_io_expansion_service(
                 append_args=[
                     "--defaultEnvironmentType=PROCESS",
                     "--defaultEnvironmentConfig={\"command\":\"/opt/apache/beam_java/boot\"}",
                 ]
             )
         )
         | 'AddReadField' >> beam.ParDo(AddReadField())
         | 'WriteToKafka' >> WriteToKafka(
             producer_config=kafka_config,
             topic='test-output-beam',
             expansion_service=default_io_expansion_service(
                 append_args=[
                    "--defaultEnvironmentType=PROCESS",
                    "--defaultEnvironmentConfig={\"command\":\"/opt/apache/beam_java/boot\"}",
                ]
            )
         ))


if __name__ == '__main__':
    run()
