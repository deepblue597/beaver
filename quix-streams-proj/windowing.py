from datetime import timedelta
from quixstreams import Application
from quixstreams.models import TopicConfig

app = Application(
    broker_address="localhost:39092",  # Kafka broker address
    auto_offset_reset="earliest",
    consumer_group="windowing",
)

# Define the Kafka topics
wikipedia_topic = app.topic("wikipedia-events", value_deserializer="json")
windowing = app.topic("windowing", value_serializer="json")
windowing_final = app.topic("windowing-final", value_serializer="json")

sdf = app.dataframe(topic=wikipedia_topic)
sdf['len_diff'] = sdf['new_length'] - sdf['old_length']

sdflen = (
    sdf.apply(lambda event: event["len_diff"])
    .tumbling_window(timedelta(seconds=2))
    .sum()
    .final()
    .apply(lambda result: {
        "sum_length": result["value"],
        "window_start_ms": result["start"],
        "window_end_ms": result["end"],
    })
)


sdf = (
    # Extract "temperature" value from the message

    sdf.apply(lambda event: event["len_diff"])

    # Define a tumbling window of 1 hour
    # You can also pass duration_ms as an integer of milliseconds
    .tumbling_window(duration_ms=timedelta(milliseconds=1))

    # Specify the "mean" aggregate function
    .mean()

    # Emit updates for each incoming message
    .current()  # .current()  # and use .final() to emit results only when the window is complete

    # Unwrap the aggregated result to match the expected output format #TODO: Test it
    .apply(
        lambda result: {
            "avg_len_diff": result["value"],
            "window_start_ms": result["start"],
            "window_end_ms": result["end"],
        }
    )
)

# sdflen = sdflen.tumbling_window(timedelta(seconds=1)).sum().final().apply(lambda result: {
#     "sum_length": result["value"],
#     "window_start_ms": result["start"],
#     "window_end_ms": result["end"], })

# sdf = sdf.to_topic(windowing)
sdflen = sdflen.to_topic(windowing_final)
# Run the streaming application (app automatically tracks the sdf!)
app.run()
