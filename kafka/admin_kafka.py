from confluent_kafka.admin import (AdminClient, NewTopic, NewPartitions, ConfigResource,
                                   ConfigEntry, ConfigSource, AclBinding,
                                   AclBindingFilter, ResourceType, ResourcePatternType,
                                   AclOperation, AclPermissionType, AlterConfigOpType,
                                   ScramMechanism, ScramCredentialInfo,
                                   UserScramCredentialUpsertion, UserScramCredentialDeletion,
                                   OffsetSpec)
from kafka_server_funcs import parse_command_line_arguments


def example_create_topics(a: AdminClient, topics: list[str], num_partitions: int = 3,  rep_factor: int = 1) -> None:
    """ Create topics """

    new_topics = [NewTopic(topic, num_partitions=num_partitions,
                           replication_factor=rep_factor) for topic in topics]
    # Call create_topics to asynchronously create topics, a dict
    # of <topic,future> is returned.
    fs = a.create_topics(new_topics)

    # Wait for operation to finish.
    # Timeouts are preferably controlled by passing request_timeout=15.0
    # to the create_topics() call.
    # All futures will finish at the same time.
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print("Topic {} created".format(topic))
        except Exception as e:
            print("Failed to create topic {}: {}".format(topic, e))


def example_delete_topics(a: AdminClient, topics: list[str]):
    """ delete topics """

    # Call delete_topics to asynchronously delete topics, a future is returned.
    # By default this operation on the broker returns immediately while
    # topics are deleted in the background. But here we give it some time (30s)
    # to propagate in the cluster before returning.
    #
    # Returns a dict of <topic,future>.
    fs = a.delete_topics(topics, operation_timeout=30)

    # Wait for operation to finish.
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print("Topic {} deleted".format(topic))
        except Exception as e:
            print("Failed to delete topic {}: {}".format(topic, e))


if __name__ == "__main__":

    args = parse_command_line_arguments()

    kafkaAdmin = AdminClient({'bootstrap.servers': args.bootstrap_server})

    newTopic = ["topic-part-3"]

    # example_create_topics(kafkaAdmin, newTopic, rep_factor=3)
    example_delete_topics(kafkaAdmin, newTopic)
