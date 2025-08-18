# 🦫 User testing experience

Hello and welcome to the User testing experience of Beaver! I am really glad that you want to help me improve Beaver and your feedback is really important to me <3. With that said, I want to give you some details about this testing.

## Goal

The goal of this user testing is to get your feedback on the overall experience of using Beaver. I want to know what you like, what you don't like, and what you think could be improved.

You will be using Beaver to achieve 3 tasks:

1. **Generate a pre-configured pipeline**: You will use Beaver to generate a pipeline that is already configured for you. This will help you understand how Beaver works and what it can do.
2. **Add an algorithm or a pre-processing step**: You will add an algorithm or a pre-processing step to the pipeline. This will help you understand how to customize the pipeline and how easy it is to add new components.
3. **Create a new pipeline from scratch**: You will create a new pipeline from scratch. This will help you understand how to use Beaver to create your own pipelines and how easy it is to use.

## Instructions

1. **Install Beaver**: Follow the installation instructions in the [README](README.md) to set up Beaver on your machine.
2. **Deploy the Kafka setup**: If you don't have a Kafka setup, follow the instructions in the [Kafka setup](README.md) section.
3. **Produce the data**: Use the provided scripts to produce the data needed for the tasks. You will use the `producer.py` script to produce the data. Make sure to run it before starting the tasks. To produce the data, run the following command:

   ```bash
   python producer.py --topic_name your_topic_name
   ```

   For example for the phishing dataset, you can run:

   ```bash
   python producer.py --topic_name Pishing
   ```

4. **Complete the tasks**: Follow the instructions for each task below. You can use the provided examples and [documentation](https://deepblue597.github.io/beaver-doc/) to help you.
5. **Provide feedback**: After completing the tasks, please provide your feedback on the experience using the Google Form linked at the end of this document.

## Tasks

### Task 1: Generate a Pre-configured Pipeline

We will start simple by generating a pre-configured pipeline. This pipeline will be set up to process the data you produced in the previous step. You will use the Phishing dataset for this task. Please produce the data using the `producer.py` script as described above.

The pipeline we will use is located at `examples/linear.bvr`. This pipeline contains:

- A connector to read from the Kafka topic you produced data to.
- A StandardScaler to normalize the data.
- An ALMA classifier model for classification.
- Accuracy as the evaluation metric.
- Our target feature is `is_phishing`.

Please take a look at the file to understand its structure. After that you can generate the pipeline using the following command:

```
python beaver_cli.py generate --input examples/linear.bvr --output linear_pipeline.py
```

This will generate a Python script named `linear_pipeline.py` that contains the pipeline code.

In order to run the pipeline, you can use the following command:

```python
python linear_pipeline.py
```

This will start the pipeline and it will begin processing the data from the Kafka topic you produced to. You can find the Plotly dashboard for the pipeline at `http://localhost:8050`. You can also check the produced data in the Kafka topic using the Kafka UI at `http://localhost:8080`.

### Task 2: Add an Algorithm or Pre-processing Step

In this task, you will add a new algorithm or pre-processing step to the pipeline. You can choose to add either a new algorithm or a new pre-processing step. For example you can use the `LogisticRegression` algorithm or the `MinMaxScaler` pre-processing step. You can find all the available algorithms and pre-processing steps in the [River documentation](https://riverml.xyz/latest/api/overview/).

To add a new algorithm or pre-processing step, you will need to modify the `examples/linear.bvr` file:

- Define the new algorithm or pre-processing step in the file.
- Add the new algorithm to the pipeline definition or the pre-processing step to the data definition.
- Regenerate the pipeline using the `beaver_cli.py` script.
- Run the new pipeline to see the changes in action.

### Task 3: Create a New Pipeline from Scratch

In this task, you will create a new pipeline from scratch. You can choose any dataset you want to use, but for simplicity, we recommend using the Phishing dataset again or the Trump Approval dataset. If you want to use the Trump Approval dataset, you need to uncomment the relevant lines in the `producer.py` script to produce the data.
Remember to define the topic name you want to use for the data when you run the `producer.py` script.

You will need to create a new `.bvr` file for your pipeline. The file should include at minimum:

- A connector to read from the Kafka topic you produced data to.

- 1 or more algorithms for learning.
- 1 or more Data components.
- 1 or more Pipeline components.

I also recommend adding a metric to evaluate the performance of your pipeline.
You can use the `examples/linear.bvr` file as a reference for the structure of the file. Once you have created your `.bvr` file, you can generate the pipeline using the `beaver_cli.py` script.

## Feedback

Please provide your feedback on the user testing experience using the following Google Form:
[User Testing Feedback Form](https://forms.gle/ioLVyvruJ2KCs6wd8)

## Sources

- [Beaver Documentation](https://deepblue597.github.io/beaver-doc/)
- [River Documentation](https://riverml.xyz/latest)
- [User testing Branch](https://github.com/deepblue597/thesis/tree/user_testing)
- [Beaver Repository](https://github.com/deepblue597/thesis)
