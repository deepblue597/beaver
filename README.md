# :penguin: Penguin

<p align="center">
  <img src="pinguin_logo_2.png" />
</p>

## :memo: Description

Penguin is a DSL language designed for machine learning in live data. It is designed to make the the process of retrieving, storing, filtering data as well as training models easy and accessible to everybody.

## :ocean: Quickstart

To create your first pipeline we will start with a classification example which can be found in `classification.jsl`

```
pipeline MyPipeline {
    kafka {
        broker: "localhost:9092"
        input_topic: "wikipedia-events"
        output_topic: "filtered-wikipedia-events"
        consumer_group: "wikipedia-model"
    }
    model {
        preprocessing:  StandardScaler
        type : tree
        name: HoeffdingTreeClassifier
        params: {
            grace_period = 100
            delta = 1e-1
            nominal_attributes='elevel' 'car'
        }
    }

    features {

        raw_featues : {
            domain
            namespace
            title
            comment
            user_name
            new_length
            old_length
            minor
        }

        generated_features: {

            test = 16 - q;
            len_diff = new_length - old_length;
        }

    }



    metrics : {
        MAE
        Accuracy
    }

    target {
        name: "user_type"
        mapping {
            bot: 1
            human: 0
        }
    }
}
```

First of all we have the name of the pipeline ( in this case **MyPipeline** ). It is the ID of the pipeline so the `python.template` can identify it.

**kafka** is the identifier for the kafka configuration. The user can define the broker from where the data will be retrieved, the input topic, the output topic and consumer group of the pipeline. We assume that Kafka is already configured. Below we will have instructions on how to setup your own kafka infrastructure

**model** is the River model that we will use. The user has to define the type of the algorithm, the name of the model and can also modify the default parameters of the model. Furthermore, the user can define a preprocessing step.

**features** are the characteristics that we will use from the data. You have to define at least one feature in **raw_features** which are the original characteristics that we get from the data. Additionaly the user can define new features using the **generated_features** attribute. This is an optinal attribute.

**metrics** are the metrics that will be used to score the performance of the model. The user can add one or more metrics.

**target** the target attribute is used for classification purposes. The user will need to string values of the targets to some int values.

## Tools that are being used

- Apache Kafka
- Quix streams
- River
- Docker
- Cassandra
- Text-X

A visual representation of the process that will be built is displayed below

```mermaid
graph LR
    IOT[IOT Devices] -->|Data| Kafka
    Kafka -->|Stream Data| Quix[Quix Streams]
    Quix -->|Filtered Data| River
	River -->|ML Results| Cassandra
    Kafka --> |Aggregated Data| Cassandra
```

Below i will explain each tool and its usage for the project

## :books: Penguin language

Penguin is a domain-specific language designed to define and configure data processing pipelines. The language allows users to specify various components of a pipeline, including Kafka configurations, machine learning models, features, metrics, targets, and plotting options.

### Grammar Overview

The `jsl.tx` file defines the grammar for the JSL language. Below is an overview of the main components:

- **Pipeline**: The top-level construct that defines a data processing pipeline.
- **Kafka**: Configuration for Kafka, including broker address, input and output topics, and consumer group.
- **Model**: Definition of the machine learning model, including preprocessing, model type, name, and parameters.
- **Feature**: Specification of the features used in the model.
- **Metric**: Definition of the evaluation metrics.
- **Target**: Specification of the target variable and optional mappings.
- **Plot**: Configuration for plotting the results.

## :open_file_folder: Kafka

### Purpose

The kafka folder contains scripts and configurations for setting up and managing a Kafka environment. This includes producing and consuming messages, as well as administrative tasks such as creating and deleting topics. The folder also includes a Docker Compose file for setting up a Kafka cluster using Docker.

### Files

#### admin_kafka.py

Contains functions for Kafka administrative tasks using the confluent_kafka library.
Functions include creating and deleting topics.
Example usage of AdminClient to manage Kafka topics.
consumer2.py

Script for consuming messages from a Kafka topic.
Uses the confluent_kafka library to create a Kafka consumer.
Includes logic for handling messages and closing the consumer gracefully.

#### docker-compose.yml

Docker Compose configuration file for setting up a Kafka cluster.
Defines services for Kafka controllers and brokers.
Includes environment variables and dependencies for each service.
Also includes a Kafka UI service for managing the Kafka cluster.

#### kafka_server_funcs.py

Contains utility functions for parsing command-line arguments.
Used by other scripts to standardize argument parsing.

#### producer_v2.py

Script for producing messages to a Kafka topic.
Uses the confluent_kafka library to create a Kafka producer.
Includes functions for constructing events and IDs, initializing namespaces, and handling delivery callbacks.
Parses command-line arguments to configure the producer.

## Quix Streams

This directory contains various scripts and modules for processing and analyzing streaming data using Kafka and Quix Streams.

#### **init**.py

An empty file that indicates that the directory should be treated as a Python package.

#### kafka_test.py

A script for testing Kafka integration with Quix Streams. It reads data from a Kafka topic, processes it, and writes the results to different Kafka topics. The script includes examples of filtering, dropping columns, and producing alerts.

#### windowing.py

A script that demonstrates windowing operations on streaming data using Quix Streams. It reads data from a Kafka topic, applies tumbling windows, and computes aggregate functions such as sum and mean. The results are then written to another Kafka topic.

## :page_with_curl: wikimedia

This directory is a project for processing and analyzing Wikimedia streaming data using Kafka, Quix Streams and River.

### HoeffdingTreeClassifier.pkl

A serialized file containing the trained `HoeffdingTreeClassifier` model. This model is used for predicting whether a user is a bot or a human based on Wikimedia event data.

### model.py

A script for training a `HoeffdingTreeClassifier` model using streaming data from a Kafka topic. The script reads data from the `wikipedia-events` Kafka topic, processes it, trains the model, and writes the results to the `filtered-wikipedia-events` Kafka topic.

### prediction.py

A script for loading the trained `HoeffdingTreeClassifier` model and using it to make predictions on new data. The script includes an example of predicting whether a user is a bot or a human based on a sample Wikimedia event.

### producer.py

A script for producing Wikimedia event data to a Kafka topic. The script consumes data from the Wikimedia EventStreams API, processes it, and produces messages to the `wikipedia-events` Kafka topic.

## :hammer: Setup your Kafka infrastructure

`kafka_proj` folder contains all the necessary files to create your own kafka infrastructure. What you will need is run `docker-compose.yml` using

```bash
docker compose up docker-compose.yml
```

This will create a Kafka infrastructure with 3 brokers and 3 controllers. You can check your configuration at `localhost:8080`
