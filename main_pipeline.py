from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud import pubsub_v1
from google.cloud import bigquery
import apache_beam as beam
import logging
import argparse
from datetime import datetime
import sys
import re
import time


PROJECT = "simple-data-pipeline-254314"
SCHEMA = 'ticker:STRING, latest_time:TIMESTAMP, latest_price:FLOAT'
TOPIC = "projects/{project}/topics/simple-data-pipeline-topic".format(project=PROJECT)


class Split(beam.DoFn):

    message = """{ticker},{epoch_timestamp},{price}"""

    def _epoch_to_datetime(self, epoch):
        datetime_string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))
        return datetime_string

    def process(self, element):
        element = element.split(",")
        ticker_identifier = element[0]
        epoch = float(element[1])
        latest_price = float(element[2])
        datetime_string = self._epoch_to_datetime(epoch)
        return [{
            'ticker': ticker_identifier,
            'latest_time': datetime_string,
            'latest_price': latest_price,
        }]


def main(argv=None):

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_topic")
    parser.add_argument("--output")
    known_args = parser.parse_known_args(argv)
    p = beam.Pipeline(options=PipelineOptions())
    (p
       | 'ReadData' >> beam.io.ReadFromPubSub(topic=TOPIC).with_output_types(bytes)
       | "Decode" >> beam.Map(lambda x: x.decode('utf-8'))
       | 'ParseCSV' >> beam.ParDo(Split())
       | 'WriteToBigQuery' >> beam.io.WriteToBigQuery('{0}:userlogs.streaminglogs'.format(PROJECT), schema=SCHEMA, write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
    )
    result = p.run()
    result.wait_until_finish()


if __name__ == '__main__':
    logger = logging.getLogger().setLevel(logging.INFO)
    main()
