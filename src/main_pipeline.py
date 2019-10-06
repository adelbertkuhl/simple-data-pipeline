import os
import logging
import argparse

from apache_beam.options.pipeline_options import PipelineOptions
import apache_beam as beam

PROJECT = os.environ.get('PROJECT')
TOPIC = os.environ.get('TOPIC')
SCHEMA = 'ticker:STRING, latest_time:TIMESTAMP, latest_price:FLOAT'
TOPIC_PATH = "projects/{project}/topics/{topic}".format(project=PROJECT, topic=TOPIC)
DATASET = 'simple_data_pipeline_dataset'
TABLE = 'simple_data_pipeline_bitcoin'


class Split(beam.DoFn):

    def _epoch_to_datetime(self, epoch):
        from datetime import datetime
        datetime_output = datetime.fromtimestamp(epoch / 1000)
        return datetime_output.strftime("%Y-%m-%d %H:%M:%S")

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


def run(argv=None):

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_topic")
    parser.add_argument("--output")
    known_args = parser.parse_known_args(argv)
    p = beam.Pipeline(options=PipelineOptions())
    messages = (p | 'ReadData' >> beam.io.ReadFromPubSub(topic=TOPIC_PATH).with_output_types(bytes))
    lines = (messages | "Decode" >> beam.Map(lambda x: x.decode('utf-8')))
    data = (lines | 'ParseDelimitedData' >> beam.ParDo(Split()))
    (data | 'WriteToBigQuery' >> beam.io.WriteToBigQuery(
        '{project}:{dataset}.{table}'.format(project=PROJECT, dataset=DATASET, table=TABLE),
        schema=SCHEMA,
        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
    )
    result = p.run()
    result.wait_until_finish()


if __name__ == '__main__':
    logger = logging.getLogger().setLevel(logging.INFO)
    run()
