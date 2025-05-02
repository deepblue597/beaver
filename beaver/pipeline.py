from typing import Union
import dill
from matplotlib import pyplot as plt
from river import metrics
from typing import List
from collections import deque

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
    y : str, optional 
        The target y value
    output_topic : str, optional
        The Kafka topic to which the output will be sent. Default is None.

    """

    def __init__(self, model, name: str,  metrics_list: List[metrics.base.Metric] = None, y: str = None, output_topic: str = None):
        self.y = y
        self.model = model
        self.output_topic = output_topic
        self.name = name
        self.metrics_list = metrics_list
        self.forecast_queue = deque(maxlen=2)
        self.passed_seasonality = 0
        """
        Best Practices
            - Group Metrics by Type:
            - Use separate Metrics containers for classification, regression, and clustering metrics.
            - Some classification metrics need probabilities these will have requires_labels → False     check KNNClassifier.py So 4th container probabilities_classification
        """
        if self.metrics_list is not None:
            self.metrics = {
                'probabilistic': None,
                'classification': None,
                'regression': None,
                'clustering': None, }
            # print(self.model)
            for metric in metrics_list:
                # print(metric)
                if hasattr(metric, "requires_labels") and not metric.requires_labels:
                    if self.metrics['probabilistic'] is None:
                        try:
                            # Check if model.predict_proba_one() is implemented
                            model.predict_proba_one()
                        except NotImplementedError:
                            raise NotImplementedError(
                                f"{model.__class__.__name__} does not support probabilistic metrics.")
                        self.metrics['probabilistic'] = metric
                    else:
                        self.metrics['probabilistic'] += metric
                elif issubclass(metric.__class__, metrics.base.ClassificationMetric):

                    if self.metrics['classification'] is None:
                        print(metric)
                        self.metrics['classification'] = metric
                    else:
                        # print(metric)
                        self.metrics['classification'] += metric
                elif issubclass(metric.__class__, metrics.base.RegressionMetric):
                    if self.metrics['regression'] is None:
                        self.metrics['regression'] = metric
                    else:
                        self.metrics['regression'] += metric
                elif issubclass(metric.__class__, metrics.base.ClusteringMetric):
                    if self.metrics['clustering'] is None:
                        self.metrics['clustering'] = metric
                    else:
                        self.metrics['clustering'] += metric
                else:
                    raise ValueError(
                        f"Unknown metric type: {metric.__class__.__name__}")
            self.metrics_values = {
                metric.__class__.__name__: [] for metric in self.metrics_list
            }

    def __str__(self):
        return f"Pipeline: {self.name}, Model: {self.model}, Metrics: {self.metrics}, Output Topic: {self.output_topic}"

    def train_and_predict(self, X) -> dict:
        """
        Train the model on the input data and make predictions.
        Add the values of metrics into a list and return a dict containing the 
        input data the prediction and the metrics values.
        """
        """We need to check if : 
        
        - [X] model is supervised or not 
        - [X] the metrics are multiclass or not 
        
        """
        y = None
        y_predicted_proba = None
        # If y exists we need to seperate it from the data
        if self.y:
            # If the model is supervised, we need to separate the features and the target variable
            y = X[self.y]
            X = {key: value for key, value in X.items() if key != self.y}

        # Train the model
        if self.model._supervised:
            self.model.learn_one(x=X, y=y)
        else:
            self.model.learn_one(x=X)

        # There are classes that do not support predict_one.
        # We need to support these classes too
        """
        FIXME:
        - [] Forecaster -> def forecast(self, horizon: int, xs: list[dict] | None = None)
        forecast = model.forecast(horizon=horizon)
        - [X] Anomaly detection -> score_one(x: dict, y: base.typing.Target) 
        
        """
        # Predict the class
        try:
            y_predicted = self.model.predict_one(X)
        except AttributeError:
            y_predicted = self.model.score_one(X)

        # Predict the probabilities
        if self.metrics['probabilistic'] is not None:
            y_predicted_proba = self.model.predict_proba_one(X)

        # TODO: Add this to function and remove the predict_class part
        # y_predicted, y_predicted_proba = self.predict(X)

        """
        If there are not metrics we dont run this code 
        also if there are no predictions we dont run this code 
        """
        if self.metrics_list is not None and (y_predicted is not None or y_predicted_proba is not None):
            for metric in self.metrics:
                if self.metrics[metric] is not None:

                    if metric == 'probabilistic':
                        # Update the probabilistic metrics
                        self.metrics[metric].update(y, y_predicted_proba)
                    else:  # Update the metrics
                        self.metrics[metric].update(y, y_predicted)

        # Store the metrics values
        for metric in self.metrics_list:
            # print(f"{metric.__class__.__name__}:{metric.get()}")
            self.metrics_values[metric.__class__.__name__].append(metric.get())

        # Save the model to a file
        with open(f'{self.name}.pkl', 'wb') as model_file:
            dill.dump(self.model, model_file)

        output = {**X}
        if y is not None:
            output['y_true'] = y
        if y_predicted_proba is not None:
            output['y_predicted_probabilities'] = y_predicted_proba
        if y_predicted is not None:
            output['y_predicted'] = y_predicted
        if self.metrics_list is not None:
            output['metrics'] = {key: values[-1]
                                 for key, values in self.metrics_values.items()}

        return output

    def metrics_plot(self):
        """
        Plot the metrics values.
        """
        for metric_name, values in self.metrics_values.items():
            plt.plot(values, label=metric_name)
            plt.title(f"{self.name} - {metric_name}")
        plt.legend()
        plt.show()

    def predict(self, X) -> Union[float, List[float]]:
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
        y_predicted, y_predicted_proba = None
        self.passed_seasonality += 1
        if hasattr(self.model, "predict_one"):
            y_predicted = self.model.predict_one(X)

        elif hasattr(self.model, "score_one"):
            y_predicted = self.model.score_one(X)

        elif hasattr(self.model, "forecast"):
            seasonal_pattern = self.model.seasonality if hasattr(
                self.model, "seasonality") else self.model.m
            if self.passed_seasonality > seasonal_pattern:
                self.forecast_queue.append(self.model.forecast(horizon=1)[0])
            if self.passed_seasonality > seasonal_pattern + 1:
                y_predicted = self.forecast_queue.popleft()

        # For probabilistic metrics
        if self.metrics['probabilistic'] is not None:
            y_predicted_proba = self.model.predict_proba_one(X)

        return y_predicted, y_predicted_proba
