# %%
import pandas as pd
from river import datasets
import pandas as pd
from kafka_proj.producer_v2 import parse_command_line_arguments, create_kafka_producer, delivery_callback
# %%

def convert_keys_to_underscores(data):
    """
    Recursively converts all dictionary keys by replacing spaces with underscores.
    """
    if isinstance(data, dict):
        return {
            key.replace(" ", "_").lower(): convert_keys_to_underscores(value)
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [convert_keys_to_underscores(item) for item in data]
    else:
        return data

if __name__ == "__main__":

    args = parse_command_line_arguments()

    # init producer
    producer = create_kafka_producer(
        bootstrap_server=args.bootstrap_server, acks='all',  compression_type='snappy')
# %%
    
    # Task 1: Phishing dataset 
    dataset = datasets.Phishing()
    
    # Task 3: Trump Approval dataset
    #dataset = datasets.TrumpApproval()

# %%
    # Trump approval , Airline , Phising
    df = pd.read_csv(dataset.path)
# %%
    df

# %%
    print('Messages are being published to Kafka topic')
    messages_count = 0

    for idx, row in df.iterrows():

        
        # convert to json format
        #Trump Approval dataset 
        json_message = row.to_json()

        # Produce the message to kafka
        producer.produce(
            args.topic_name, value=json_message, key=str(idx), callback=delivery_callback)

        # Polling to handle responses
        producer.poll(0)

        messages_count += 1

    # Flush to ensure all messages are sent before exit
    producer.flush()
