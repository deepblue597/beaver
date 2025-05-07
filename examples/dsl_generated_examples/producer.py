# %%
import json
import pandas as pd
from river import datasets, preprocessing
import kagglehub
import pandas as pd
from river.datasets import synth

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
    #dataset = datasets.TrumpApproval()
    # dataset = datasets.ImageSegments()
    # print("Path to dataset files:", path)
    # gen = synth.Agrawal(classification_function=0, seed=42)
    # gen = synth.ConceptDriftStream(stream=synth.SEA(seed=42, variant=0),
    #                                drift_stream=synth.SEA(seed=42, variant=1),
    #                                seed=1, position=500, width=50)
    # dataset = iter(gen.take(1000))
    # dataset = synth.ConceptDriftStream(
    #    seed=42,
    #    position=500,
    #    width=40).take(1000)
    # dataset = datasets.Bananas().take(500)
    # dataset = [
    #     [1, 2],
    #     [1, 4],
    #     [1, 0],
    #     [-4, 2],
    #     [-4, 4],
    #     [-4, 0],
    #     [5, 0],
    #     [5, 2],
    #     [5, 4]
    # ]
    #dataset = datasets.AirlinePassengers()
# %%
    dataset

# %%
    # csv_path = os.path.join(path, "boston.csv")
    # Trump approval
    #df = pd.read_csv(dataset.path)
    # Bananas, Clustering
    df = pd.DataFrame(dataset)
# %%
    df
    
#%% 

# for idx, row in df.iterrows():
#     json_message = row.to_json()
#     #sample_dict = {**row[0].isoformat(), 'passengers': row[1]}
#     print(json_message)
# %%
    print('Messages are being published to Kafka topic')
    messages_count = 0

    for idx, row in df.iterrows():

        # bananas
        sample_dict = {**row[0], 'class': row[1]}
        # convert to json format
        # TRump
        #json_message = row.to_json()
        json_message = json.dumps(sample_dict)

        # Produce the message to kafka
        producer.produce(
            args.topic_name, value=json_message, key=str(idx), callback=delivery_callback)

        # Polling to handle responses
        producer.poll(0)

        messages_count += 1

    # Flush to ensure all messages are sent before exit
    producer.flush()
