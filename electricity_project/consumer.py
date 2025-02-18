from quixstreams import Application
from quixstreams.models import TopicConfig
from river import time_series
import calendar
import math
import pickle
from river import compose
from river import linear_model
from river import optim
from river import preprocessing
import datetime
import dill


# A minimal application reading temperature data in Celsius from the Kafka topic,
# converting it to Fahrenheit and producing alerts to another topic.

# Define an application that will connect to Kafka
app = Application(
    broker_address="localhost:39092",  # Kafka broker address
    auto_offset_reset="earliest",
    consumer_group="model-electricity-snarimax",
)

# Topics from which the application will read and write
read_topic = app.topic("electricity-24", value_deserializer="json")
write_topic = app.topic("model-hist-var-24",
                        value_serializer="json")


# Create a Streaming DataFrame connected to the input Kafka topic
sdf = app.dataframe(topic=read_topic)

# select only the columns we need
sdf_filtered = sdf[['Datetime (UTC)', 'Carbon Intensity gCO₂eq/kWh (direct)']]


# you can load the model from a file
# with open('SNARIMAX_electricity_h.pkl', 'rb') as model_file:
#     model = pickle.load(model_file)

# Define the model

def get_hour_distances(x):
    hour = x.hour  # Extract hour from the datetime object
    return {
        f"hour_{h}": math.exp(-(hour - h) ** 2) for h in range(24)
    }


def get_ordinal_date(x):
    return {'ordinal_date': x.toordinal()}


extract_features = compose.TransformerUnion(
    get_ordinal_date,
    get_hour_distances
)

model = (
    extract_features |
    time_series.SNARIMAX(
        p=1,
        d=1,
        q=1,
        m=24,
        sd=1,
        sp=6,
        sq=12,
        regressor=(
            preprocessing.StandardScaler() |
            linear_model.LinearRegression(
                intercept_init=110,
                optimizer=optim.SGD(0.01),
                intercept_lr=0.3
            )
        )
    )
)


# Function to train the model on each row of data


def train_and_predict(row):

    y = row['Carbon Intensity gCO₂eq/kWh (direct)']
    x = datetime.datetime.strptime(row['Datetime (UTC)'], "%Y-%m-%d %H:%M:%S")

    # Train the model
    # model.learn_one(x, y)
    model.learn_one(x, y)

    # print('model updated')

    with open('SNARIMAX_electricity_h.pkl', 'wb') as model_file:
        dill.dump(model, model_file)

    print('model saved')

    return row


# Apply the train_and_predict function to each row in the filtered DataFrame
sdf_filtered = sdf_filtered.apply(train_and_predict)

# Write the filtered DataFrame to the output Kafka topic
sdf_filtered = sdf_filtered.to_topic(write_topic)


# Run the streaming application (app automatically tracks the sdf!)
app.run()
