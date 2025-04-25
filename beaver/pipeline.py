# TODO: Create a pipeline class
from typing import Union
import dill
from matplotlib import pyplot as plt
from river import metrics

__all__ = ['Pipeline']


class Pipeline:
    """
    A class to represent a machine learning pipeline.

    In order to compartmentalize the functionality of each pipeline. 
    we create a class that has all the attributes and functions that are needed to run a pipeline.

    Parameters
    ----------
    model : object
        The machine learning model to be used in the pipeline.
    metrics : list
        A list of metrics to evaluate the model's performance.
    name : str
        The name of the pipeline.
    output_topic : str, optional
        The Kafka topic to which the output will be sent. Default is None.

    """

    def __init__(self, model, metrics_list: list, name: str,  output_topic: str = None):
        self.model = model
        self.output_topic = output_topic
        self.name = name
        self.metrics_list = metrics_list
        """
        Best Practices
            - Group Metrics by Type:
            - Use separate Metrics containers for classification, regression, and clustering metrics.
            - Some classification metrics need probabilities these will have requires_labels → False     check KNNClassifier.py So 4th container probabilities_classification
            TODO:The multioutput metrics cannot be added to one metric. Need to be separate.
        """
        self.metrics = {
            'classification': None,
            'regression': None,
            'clustering': None, }
        self.probabilistc = False
        # FIXME:
        for metric in self.metrics_list:
            if not metric.requires_labels and not self.probabilistc:
                try:
                    # Check if model.predict_proba_one() is implemented
                    model.predict_proba_one()
                except NotImplementedError:
                    raise NotImplementedError(
                        f"{model.__class__.__name__} does not support probabilistic metrics.")
                self.probabilistc = True

            elif issubclass(metric, metrics.base.ClassificationMetric):
                if self.metrics['classification'] is None:
                    self.metrics['classification'] = metric
                else:
                    self.metrics['classification'].__add__(metric)
            elif issubclass(metric, metrics.base.RegressionMetric):
                if self.regression_metrics is None:
                    self.regression_metrics = metric
                else:
                    self.regression_metrics.__add__(metric)
            elif issubclass(metric, metrics.base.ClusteringMetric):
                if self.clustering_metrics is None:
                    self.clustering_metrics = metric
                else:
                    self.clustering_metrics.__add__(metric)
            else:
                raise ValueError(
                    f"Unknown metric type: {metric.__class__.__name__}")
        self.metrics_values = {
            metric.__class__.__name__: [] for metric in self.metrics_list
        }

    def __str__(self):
        return f"Pipeline: {self.name}, Model: {self.model}, Metrics: {self.metrics}, Output Topic: {self.output_topic}"

    def train_and_predict(self, X, y: str = None) -> dict:
        """
        Train the model on the input data and make predictions.
        Add the values of metrics into a list and return a dict containing the 
        input data the prediction and the metrics values.
        """
        """TODO: We need to check if : 
        
        - [] model is supervised or not 
        - [] the metrics are multiclass or not 
        
        """
        if self.model._supervised:
            # If the model is supervised, we need to separate the features and the target variable
            y = X[y]
            X = {key: value for key, value in X.items() if key != y}

        # Train the model
        if self.model._supervised:
            self.model.learn_one(X, y)
        else:
            self.model.learn_one(X)

        # Predict the class
        y_predicted = self.model.predict_one(X)

        # Update metrics
        self.metrics.update(y, y_predicted)

        # Store the metrics values
        for metric in self.metrics_list:
            self.metrics_values[metric.__class__.__name__].append(metric.get())

        # Save the model to a file
        with open(f'{self.name}.pkl', 'wb') as model_file:
            dill.dump(self.model, model_file)

        return {
            **X,
            **({'y_true': y} if y is not None else {}),
            'y_predicted': y_predicted,
            'metrics': {metric.__class__.__name__: metric.get() for metric in self.metrics}

        }

    def metrics_plot(self):
        """
        Plot the metrics values.
        """
        for metric_name, values in self.metrics_values.items():
            plt.plot(values, label=metric_name)
        plt.legend()
        plt.show()
