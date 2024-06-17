import os
import posixpath

import apache_beam as beam
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions


def run():
    working_path = os.path.dirname(__file__)

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
    ])

    with beam.Pipeline(options=options) as p:
        (p
            | 'Create words' >> beam.Create(['to be or not to be'])
            | 'Split words' >> beam.FlatMap(lambda words: words.split(' '))
            | 'Write to file' >> WriteToText('test.txt')
        )


if __name__ == "__main__":
    run()
