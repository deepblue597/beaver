import time
import requests
import json

from kafka_proj.producer_v2 import create_kafka_producer, delivery_callback, parse_command_line_arguments


def fetch_live_data(producer, url, headers, args, messages_count):

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        print(data)  # Print or process the data
        id = json.dumps({"id": messages_count}).encode('utf-8')
        producer.produce(
            args.topic_name, value=json.dumps(data).encode('utf-8'), key=id, callback=delivery_callback)

        producer.poll(0)
        # producer.flush()  # Ensure the producer sends the message before proceeding

        messages_count += 1

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")


def on_termination(producer):

    producer.flush()


def main():
    polling_interval = 1800  # Fetch data every 30 minutes
    messages_count = 0  # Count of messages produced
    args = parse_command_line_arguments()

    # init producer
    producer = create_kafka_producer(bootstrap_server=args.bootstrap_server,
                                     acks='all', linger_ms=20, batch_size=32 * 1024, compression_type='snappy')

    url = "https://api.electricitymap.org/v3/carbon-intensity/latest?zone=FR"
    headers = {"auth-token": "cVbydpxzZLhtoYbTsaaV"}

    try:

        while True:
            fetch_live_data(producer, url, headers, args, messages_count)
            messages_count += 1
            time.sleep(polling_interval)

    except KeyboardInterrupt:
        on_termination(producer)  # Run custom logic on interrupt
    finally:
        print("Exiting gracefully.")


if __name__ == "__main__":
    main()
