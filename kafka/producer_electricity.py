import pandas as pd


from producer_v2 import parse_command_line_arguments, create_kafka_producer, delivery_callback


if __name__ == "__main__":

    args = parse_command_line_arguments()

    # init producer
    producer = create_kafka_producer(
        bootstrap_server=args.bootstrap_server, acks='all',  compression_type='snappy')

    # read the data from the combined file.
    data = pd.read_csv('combined_file.csv')

    print('Messages are being published to Kafka topic')
    messages_count = 0

    for idx, row in data.iterrows():

        json_message = row.to_json()
        producer.produce(
            args.topic_name, value=json_message, key=str(idx), callback=delivery_callback)
        # Polling to handle responses

        producer.poll(0)

        messages_count += 1
        if messages_count >= args.events_to_produce:
            print('Producer will be killed as {} events were producted'.format(
                args.events_to_produce))
            break
    # Flush to ensure all messages are sent before exit
    producer.flush()
