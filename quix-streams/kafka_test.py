from quixstreams import Application
from quixstreams.models import TopicConfig


# A minimal application reading temperature data in Celsius from the Kafka topic,
# converting it to Fahrenheit and producing alerts to another topic.

# Define an application that will connect to Kafka
app = Application(
    broker_address="localhost:39092",  # Kafka broker address
    auto_offset_reset="earliest",
    consumer_group="bot_events",
)

# Define the Kafka topics
wikipedia_topic = app.topic("wikipedia-events", value_deserializer="json")
bot_topic = app.topic("bot-events", value_serializer="json")
simple_topic = app.topic("simple_topic", value_serializer="json")
drop_topic = app.topic("drop_topic", value_serializer="json")

# Create a Streaming DataFrame connected to the input Kafka topic
sdf = app.dataframe(topic=wikipedia_topic)


# select only the columns we need
sdf_simple = sdf[['title', 'comment', 'timestamp', 'user_name']]

# Filter values from bot
sdf = sdf[sdf["user_type"] == 'bot']

# Drop values
sdf_drop = sdf.drop(["id", "title", "comment", "user_name"])

# add a new column with the length diff
sdf_drop['len_diff'] = sdf_drop['new_length'] - sdf_drop['old_length']

# Produce alerts to the output topic
sdf = sdf.to_topic(bot_topic)
sdf_simple = sdf_simple.to_topic(simple_topic)
sdf_drop = sdf_drop.to_topic(drop_topic)


# Run the streaming application (app automatically tracks the sdf!)
app.run()
