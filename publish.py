import os
import threading

from google.cloud import pubsub_v1
from request_executors import RequestExecutor

PROJECT = os.environ.get('PROJECT')
TOPIC = os.environ.get('TOPIC')
WAIT_TIME_SECONDS = 60

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT, TOPIC)


class PricePublisher:

    def __init__(self, publisher_class, topic_path_object):
        self.publisher = publisher_class
        self.topic_path = topic_path_object

    def publish(self, message):
        data = message.encode('utf-8')
        return self.publisher.publish(self.topic_path, data=data)

    def callback(self, message_future):
        if message_future.exception(timeout=30):
            print('Publishing message on {} threw an Exception {}.'.format(
                topic_name, message_future.exception()))
        else:
            print(message_future.result())

    def run(self, message):
        message_future = self.publish(message)
        message_future.add_done_callback(self.callback)


if __name__ == '__main__':
    executor = RequestExecutor()
    price_publisher = PricePublisher(publisher, topic_path)
    ticker = threading.Event()
    while not ticker.wait(WAIT_TIME_SECONDS):
        data = executor.retrieve_price_data()
        print(data)
        price_publisher.run(data)
