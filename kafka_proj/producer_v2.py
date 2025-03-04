import json
import argparse

from confluent_kafka import Producer
from sseclient import SSEClient as EventSource
# from kafka import RoundRobinPartitioner


# https://docs.confluent.io/platform/current/clients/producer.html
# https://docs.confluent.io/platform/current/installation/configuration/producer-configs.html
def create_kafka_producer(bootstrap_server, acks, linger_ms=0, batch_size=16 * 1024, compression_type=None):
    config = {
        # User-specific properties that you must set
        'bootstrap.servers': bootstrap_server,
        # 'partitioner': RoundRobinPartitioner,
        # TODO: find out how to change number of partitions -> through kafka admin
        'acks': acks,  # 0 1 all|-1
        # 'value.serializer': lambda x: json.dumps(x).encode('utf-8')
        'batch.size': batch_size,  # default 16Kb
        # ' delivery.timeout.ms' : 120000 ( default 2 mins )
        # 'enable.idempotence': True (default)
        'linger.ms': linger_ms,  # Wait up to x ms for the batch to fill before sending default 0
        'compression.type': compression_type  # None ( default )

    }

    # not working
    # partitioner = RoundRobinPartitioner(partitions=3)  # Assume we have 3 partitions in the topic

    # Create Producer instance
    producer = Producer(config)
    return producer


def construct_id(event_data):
    event_data = {'id': event_data['id']}

    return json.dumps({"id": event_data['id']}).encode('utf-8')


def construct_event(event_data, user_types):
    # use dictionary to change assign namespace value and catch any unknown namespaces (like ns 104)
    try:
        event_data['namespace'] = namespace_dict[event_data['namespace']]
    except KeyError:
        event_data['namespace'] = 'unknown'

    # assign user type value to either bot or human
    user_type = user_types[event_data['bot']]

    # define the structure of the json event that will be published to kafka topic
    event = json.dumps({"id": event_data['id'],
                        "domain": event_data['meta']['domain'],
                        "namespace": event_data['namespace'],
                        "title": event_data['title'],
                        "comment": event_data['comment'],
                        # event_data['timestamp'],
                        "timestamp": event_data['meta']['dt'],
                        "user_name": event_data['user'],
                        "user_type": user_type,
                        "minor": event_data['minor'],
                        # "type": event_data['type'],
                        "old_length": event_data['length']['old'],
                        "new_length": event_data['length']['new']}).encode('utf-8')

    return event


def init_namespaces():
    # create a dictionary for the various known namespaces
    # more info https://en.wikipedia.org/wiki/Wikipedia:Namespace#Programming
    namespace_dict = {-2: 'Media',
                      -1: 'Special',
                      0: 'main namespace',
                      1: 'Talk',
                      2: 'User', 3: 'User Talk',
                      4: 'Wikipedia', 5: 'Wikipedia Talk',
                      6: 'File', 7: 'File Talk',
                      8: 'MediaWiki', 9: 'MediaWiki Talk',
                      10: 'Template', 11: 'Template Talk',
                      12: 'Help', 13: 'Help Talk',
                      14: 'Category', 15: 'Category Talk',
                      100: 'Portal', 101: 'Portal Talk',
                      108: 'Book', 109: 'Book Talk',
                      118: 'Draft', 119: 'Draft Talk',
                      446: 'Education Program', 447: 'Education Program Talk',
                      710: 'TimedText', 711: 'TimedText Talk',
                      828: 'Module', 829: 'Module Talk',
                      2300: 'Gadget', 2301: 'Gadget Talk',
                      2302: 'Gadget definition', 2303: 'Gadget definition Talk'}

    return namespace_dict


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description='EventStreams Kafka producer')

    parser.add_argument('--bootstrap_server', default='localhost:39092',
                        help='Kafka bootstrap broker(s) (host[:port])', type=str)
    parser.add_argument('--topic_name', default='wikipedia-events',
                        help='Destination topic name', type=str)
    parser.add_argument('--events_to_produce',
                        help='Kill producer after n events have been produced', type=int, default=500)

    return parser.parse_args()


def delivery_callback(err, msg):
    # executed when a record is successfully sent or an exception is thrown
    if err:
        print(f'ERROR: Message failed delivery: {err}')
    else:
        print(
            f"Produced event to topic {msg.topic()}: partition {msg.partition()}: value = {msg.value().decode('utf-8')}")


if __name__ == "__main__":
    # parse command line arguments
    args = parse_command_line_arguments()

    # init producer
    producer = create_kafka_producer(bootstrap_server=args.bootstrap_server,
                                     acks='all', linger_ms=20, batch_size=32 * 1024, compression_type='snappy')

    # init dictionary of namespaces
    namespace_dict = init_namespaces()

    # used to parse user type
    user_types = {True: 'bot', False: 'human'}

    # consume websocket
    url = 'https://stream.wikimedia.org/v2/stream/recentchange'

    print('Messages are being published to Kafka topic')
    messages_count = 0

    for event in EventSource(url):
        if event.event == 'message':
            try:
                event_data = json.loads(event.data)
            except ValueError:
                pass
            else:
                # filter out events, keep only article edits (mediawiki.recentchange stream)
                if event_data['type'] == 'edit':
                    # construct valid json event
                    event_to_send = construct_event(event_data, user_types)
                    id_to_send = construct_id(event_data)

                    producer.produce(
                        args.topic_name, value=event_to_send, key=id_to_send, callback=delivery_callback)
                    # Polling to handle responses
                    # do we need these ?
                    producer.poll(0)
                    # producer.flush()  # Ensure the producer sends the message before proceeding

                    messages_count += 1

        if messages_count >= args.events_to_produce:
            print('Producer will be killed as {} events were producted'.format(
                args.events_to_produce))
            break

    # Flush to ensure all messages are sent before exit
    producer.flush()
