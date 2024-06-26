import json
import logging
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
    logging.getLogger().setLevel(logging.DEBUG)

    working_path = os.path.dirname(__file__)

    # Set environment variables.
    os.environ["AWS_ACCESS_KEY"] = "minioadmin"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "minioadmin"
    os.environ["AWS_REGION"] = "us-east-1"
    # os.environ["S3_ENDPOINT"] = "http://localhost:9000"
    os.environ["S3_ENDPOINT"] = "http://minio-service.minio.svc.cluster.local:9000"

    options = PipelineOptions([
        # "--runner=DirectRunner",
        # "--environment_type=LOOPBACK",
        "--runner=FlinkRunner",
        "--flink_version=1.16",
        "--flink_master=localhost:8081",
        "--environment_type=EXTERNAL",
        "--environment_config=localhost:50000",
        f"--setup_file={posixpath.join(working_path, 'setup.py')}",
        "--streaming",
        # "--flink_submit_uber_jar",
        "--s3_region_name=us-east-1",
        "--s3_access_key_id=minioadmin",
        "--s3_secret_access_key=minioadmin",
        "--s3_endpoint=http://minio-service.minio.svc.cluster.local:9000",
        "--staging_location=s3://beam/staging",
        "--temp_location=s3://beam/temp",
    ])

    kafka_config = {
        "bootstrap.servers": "kafka-service.apache-kafka.svc.cluster.local:9093",
        "group.id": "simple-kafka-beam",
        "max.request.size": "10485760",
    }

    with beam.Pipeline(options=options) as pipeline:
        words = (
            pipeline
            | 'Create words' >> beam.Create(['to be or not to be'])
            | 'Split words' >> beam.FlatMap(lambda words: words.split(' '))
            | 'To key-value pairs' >> beam.Map(lambda word: (word.encode('utf-8'), word.encode('utf-8')))
        )

        words | 'WriteToKafka' >> WriteToKafka(
            producer_config=kafka_config,
            topic='test-output-beam',
            key_serializer='org.apache.kafka.common.serialization.ByteArraySerializer',
            value_serializer='org.apache.kafka.common.serialization.ByteArraySerializer',
            expansion_service=default_io_expansion_service(
                append_args=[
                    "--defaultEnvironmentType=PROCESS",
                    "--defaultEnvironmentConfig={\"command\":\"/opt/apache/beam_java/boot\"}",
                ]
            )
        )


if __name__ == '__main__':
    run()
