from quixstreams import Application
from quixstreams.models import TopicConfig
from river.datasets import synth
from river import evaluate
from river import metrics
from river import tree
import dill

# A minimal application reading temperature data in Celsius from the Kafka topic,
# converting it to Fahrenheit and producing alerts to another topic.

# Define an application that will connect to Kafka
app = Application(
    broker_address="localhost:39092",  # Kafka broker address
    auto_offset_reset="earliest",
    consumer_group="wikipedia-model",
)

# Define the Kafka topics
wikipedia_topic = app.topic("wikipedia-events", value_deserializer="json")
write_topic = app.topic("filtered-wikipedia-events",
                        value_serializer="json")
# Create a Streaming DataFrame connected to the input Kafka topic
sdf = app.dataframe(topic=wikipedia_topic)


model = tree.HoeffdingTreeClassifier(
    grace_period=100,
    delta=1e-1,
)

metric = metrics.MAE()

# add a new column with the length diff
sdf['len_diff'] = sdf['new_length'] - sdf['old_length']


def train_and_predict(event):

    X = {
        "domain": event["domain"],
        "namespace": event["namespace"],
        "title": event["title"],
        "comment": event["comment"],
        "user_name": event["user_name"],
        "length_change": event["len_diff"],
        "minor": int(event["minor"]),
    }
    y = 1 if event["user_type"] == "bot" else 0
    model.learn_one(X, y)

    # Prediction
    print("Prediction:", "bot" if model.predict_one(X) == 1 else "human")

    predicted_class = model.predict_one(X)

    # Update accuracy metric
    metric.update(y, predicted_class)

    print(f"True Label: {y}, Predicted: {predicted_class}")
    print(f"Current Accuracy: {metric}")

    with open('HoeffdingTreeClassifier.pkl', 'wb') as model_file:
        dill.dump(model, model_file)

    return event


# Apply the train_and_predict function to each row in the filtered DataFrame
sdf = sdf.apply(train_and_predict)


sdf = sdf.to_topic(write_topic)

# Run the streaming application (app automatically tracks the sdf!)
app.run()
