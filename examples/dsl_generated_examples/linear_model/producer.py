# %%
import pandas as pd
from river import datasets, preprocessing
import kagglehub
import pandas as pd

from kafka_proj.producer_v2 import parse_command_line_arguments, create_kafka_producer, delivery_callback
import os
# %%
if __name__ == "__main__":

    args = parse_command_line_arguments()

    # init producer
    producer = create_kafka_producer(
        bootstrap_server=args.bootstrap_server, acks='all',  compression_type='snappy')
# %%
    # path = kagglehub.dataset_download("fedesoriano/the-boston-houseprice-data")
    dataset = datasets.Phishing()
    # dataset = datasets.TrumpApproval()
    dataset = datasets.ImageSegments()
    # print("Path to dataset files:", path)
# %%
    dataset

# %%
    # csv_path = os.path.join(path, "boston.csv")
    df = pd.read_csv(dataset.path)

# %%
    df
# %%
    print('Messages are being published to Kafka topic')
    messages_count = 0

    for idx, row in df.iterrows():

        # convert to json format
        json_message = row.to_json()

        # Produce the message to kafka
        producer.produce(
            args.topic_name, value=json_message, key=str(idx), callback=delivery_callback)

        # Polling to handle responses
        producer.poll(0)

        messages_count += 1

    # Flush to ensure all messages are sent before exit
    producer.flush()
