import argparse


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description='EventStreams Kafka producer')

    parser.add_argument('--bootstrap_server', default='localhost:39092',
                        help='Kafka bootstrap broker(s) (host[:port])', type=str)
    parser.add_argument('--topic_name', default='wikipedia-events-vol2',
                        help='Destination topic name', type=str)
    parser.add_argument('--events_to_produce',
                        help='Kill producer after n events have been produced', type=int, default=400)

    return parser.parse_args()
