from collections import deque
from typing import List, Optional, Union

import dill
from matplotlib import pyplot as plt
from river import metrics
import warnings
from errors import PredictionWarning
from matplotlib.animation import FuncAnimation
import plotly.graph_objs as go

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
    metrics : list, Optional
        A list of metrics to evaluate the model's performance.
    name : str
        The name of the pipeline.
    y : str, optional 
        The target y value
    output_topic : str, optional
        The Kafka topic to which the output will be sent. Default is None.

    """

    def __init__(self,
                 model,
                 name: str,
                 metrics_list: Optional[List[metrics.base.Metric]] = None,
                 y: Optional[str] = None,
                 output_topic: Optional[str] = None
                 ):
        
        
        self.y = y
        self.model = model
        self.output_topic = output_topic
        self.name = name
        self.metrics_list = metrics_list
        
        self.passed_seasonality = 0
        """
        Best Practices
            - Group Metrics by Type:
            - Use separate Metrics containers for classification, regression, and clustering metrics.
            - Some classification metrics need probabilities these will have requires_labels → False     
                check KNNClassifier.py So 4th container probabilities_classification
        """
        if self.metrics_list is not None:
            self.metrics = {
                'probabilistic': None,
                'classification': None,
                'regression': None,
                'clustering': None, }

            # Mapping metric types to categories
            metric_type_mapping = {
                metrics.base.ClassificationMetric: 'classification',
                metrics.base.RegressionMetric: 'regression',
                metrics.base.ClusteringMetric: 'clustering',
            }
            self.metrics_values = {}

            for metric in metrics_list:
                # print(metric)
                if hasattr(metric, "requires_labels") and not metric.requires_labels:
                    if self.metrics['probabilistic'] is None:
                        try:
                            # Check if model.predict_proba_one() is implemented
                            model.predict_proba_one()
                        except NotImplementedError as exc:
                            raise NotImplementedError(
                                f"{model.__class__.__name__} does not support probabilistic metrics."
                            ) from exc
                    self._add_metric(metric, 'probabilistic')
                else:
                    # Handle other metric types using the mapping
                    for metric_class, category in metric_type_mapping.items():
                        if isinstance(metric, metric_class):
                            self._add_metric(metric, category)
                            break
                    else:
                        raise ValueError(
                            f"Unknown metric type: {metric.__class__.__name__}")

                self.metrics_values[metric.__class__.__name__] = []

    def __str__(self):
        return f"Pipeline: {self.name}, Model: {self.model}, Metrics: {self.metrics}, Output Topic: {self.output_topic}"

    def train_and_predict(self, X) -> dict:
        """
        Train the model on the input data and make predictions.
        Add the values of metrics into a list and return a dict containing the 
        input data the prediction and the metrics values.
        """
        
        y_predicted, y_predicted_proba = self._predict(X)
        #print('hi')
        # If y exists we need to seperate it from the data
        if self.y:
            y = X[self.y]
            X = {key: value for key, value in X.items() if key != self.y}

        # Train the model
        if self.model._supervised: 
            self.model.learn_one(x=X, y=y)
        else:
            self.model.learn_one(x=X)

        if self.metrics_list is not None and (y_predicted is not None or y_predicted_proba is not None): 
           
            latest_metrics = self._update_metrics(y , y_predicted , y_predicted_proba)
           
        # Save the model to a file
        with open(f'{self.name}.pkl', 'wb') as model_file:
            dill.dump(self.model, model_file)

        #TODO: Simplify these if statements
        output = {**X}
        if self.y:
            output['y_true'] = y
        if y_predicted_proba is not None:
            output['y_predicted_probabilities'] = y_predicted_proba
        if y_predicted is not None:
            output['y_predicted'] = y_predicted
        if self.metrics_list is not None and (y_predicted is not None or y_predicted_proba is not None) :
            output['metrics'] = latest_metrics

        return output

    def metrics_plot(self):
        """
        Plot the metrics values.
        """
        for metric_name, values in self.metrics_values.items():
            plt.plot(values, label=metric_name)
            plt.title(f"{self.name} - {metric_name}")
        plt.xlabel('iterations')
        plt.ylabel('values')
        plt.legend()
        plt.show()

    def _predict(self, X) -> Union[float, List[float]]:
        """
        The are 3 main cases: 

        1. The model has a predict_one method 

        This will apply to most of the cases

        2. The model has a score_one method 

        This is a model of anomaly detection type. It will score y. 
        A high score is indicative of an anomaly. A low score corresponds a normal observation. 

        3. The model has a foreact method 

        This is a forecasting algorithm. This case it the trickiest since the model 
        cannot make predictions if the data that has seen is less than the seasonality of the model. 
        Due to this we need to check if the runs have surpassed the seasonality. We will use 
        the self.passed_seasonality variable for that. It checks at which run we currently are. 
        Furhermore when we call the forecast method it predicts the next value of y. This means 
        that in order to update the metric we want the prediction of the prev. run. For that 
        we use a queue with maxlen = 2.  

        WARNING: For the seasonality check we need the seasonal pattern of the data. 
        Unfortunately this variable is different in each model. During the time of development only 
        2 models are of type forecast: HoltWinters and SNARIMAX. The models use different variables 
        for seasonality : seasonality and m. Because we need this value, if new models occur, this will 
        raise an error if the variable name is different for the seasonal pattern. 

        """
        
        y_predicted, y_predicted_proba = None, None
        
        if hasattr(self.model, "predict_one"):
            y_predicted = self.model.predict_one(X)
            
            # For probabilistic metrics
            if self.metrics['probabilistic'] is not None:
                y_predicted_proba = self.model.predict_proba_one(X)

        elif hasattr(self.model, "score_one"):
            y_predicted = self.model.score_one(X)
        
        elif hasattr(self.model, "forecast"):
            try:
                seasonal_pattern = self.model.seasonality if hasattr(
                    self.model, "seasonality") else self.model.m
            except NotImplementedError as exc:
                raise NotImplementedError(
                    f"{self.model.__class__.__name__} forecaster is not supported by beaver. Please create an issue on github.") from exc
            if self.passed_seasonality > seasonal_pattern:
                y_predicted = self.model.forecast(horizon=1)[0]
                #print(y_predicted)
        else : 
            raise NotImplementedError(f"{self.model.__class__.__name__} is not supported by beaver. Please create an issue on github.")
        
        self.passed_seasonality += 1
        #print(y_predicted)
        if y_predicted is None and y_predicted_proba is None : 
            PredictionWarning()
        
        #print(y_predicted , y_predicted_proba)
        return y_predicted, y_predicted_proba

    def _update_metrics(self, y, y_predicted, y_predicted_proba=None) -> dict:
        latest_metrics = {}
        for metric_group , metrics_in_group in self.metrics.items():
            if metrics_in_group is not None:

                if metric_group == 'probabilistic':
                    # Update the probabilistic metrics
                    metrics_in_group.update(y, y_predicted_proba)
                else:  # Update the metrics
                    metrics_in_group.update(y, y_predicted)

        # Store the metrics values
        for metric in self.metrics_list:
            metric_name = metric.__class__.__name__
            latest_value = metric.get()
            self.metrics_values[metric_name].append(latest_value)
            latest_metrics[metric_name] = latest_value

        return latest_metrics

    def _add_metric(self, metric, category):
        """Helper function to add a metric to the appropriate category."""
        if self.metrics[category] is None:
            self.metrics[category] = metric
        else:
            self.metrics[category] += metric

    def add_metrics_traces(self, fig, row=1, col=1):
        """
        Add line plot traces for each metric into the given figure.
        
        Parameters
        ----------
        fig : plotly.graph_objs.Figure
            The figure object to add traces to.
        row : int
            Row index of the subplot.
        col : int
            Column index of the subplot.
        """
        for metric_name, values in self.metrics_values.items():
            fig.add_trace(go.Scatter(
                y=values,
                mode="lines",
                name=f"{self.name} - {metric_name}"
            ), row=row, col=col)