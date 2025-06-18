from collections import deque , Counter
from typing import List, Optional, Union

import dill
from matplotlib import pyplot as plt
from river import metrics
import warnings
from beaver.errors import PredictionWarning, StatisticsWarning
from matplotlib.animation import FuncAnimation
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from river import base, utils
from sklearn.metrics import confusion_matrix
import numpy as np
from river.compose.pipeline import Pipeline as RiverPipeline
from flatten_dict import flatten

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

    def __init__(
        self,
        model,
        model_name, 
        name: str,
        metrics_list: Optional[List[metrics.base.Metric]] = None,
        y: Optional[str] = None,
        output_topic: Optional[str] = None
        ):
        
        self.model_name = model_name
        self.model_name = model_name
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
                #print(metric)
                #print(metric)
                if hasattr(metric, "requires_labels") and not metric.requires_labels:
                    if self.metrics['probabilistic'] is None:
                        try:
                            # Check if model.predict_proba_one() is implemented
                            model.predict_proba_one({})  # Test with an empty dict
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
            
        self.y_true_list = []
        self.y_pred_list = []  
            

    def __str__(self):
        return f"Pipeline: {self.name}, Model: {self.model}, Metrics: {self.metrics}, Output Topic: {self.output_topic}"

    def train_and_predict(self, X) -> dict:
        """
        Train the model on the input data and make predictions.
        Add the values of metrics into a list and return a dict containing the 
        input data the prediction and the metrics values.
        """
        X = flatten(X, reducer='underscore')
        
        y_predicted, y_predicted_proba = self._predict(X)
        #print('hi')
        # If y exists we need to seperate it from the data
        if self.y:
            y = X[self.y]
            X = {key: value for key, value in X.items() if key != self.y}

        # Train the model
        if hasattr(self.model , 'learn_one' ): 
            if self.model._supervised: 
                self.model.learn_one(x=X, y=y)
            else:
                self.model.learn_one(x=X)

        if self.metrics_list is not None and (y_predicted is not None or y_predicted_proba is not None): 
            #print('heee')
            #print('heee')
            latest_metrics = self._update_metrics(y , y_predicted , y_predicted_proba)
           
        # Save the model to a file
        with open(f'{self.name}.pkl', 'wb') as model_file:
            dill.dump(self.model, model_file)

        #TODO: Simplify these if statements
        output = {**X}
        if self.y:
            if y_predicted is not None: 
                self.y_true_list.append(y) 
            
            output['y_true'] = y
        if y_predicted_proba is not None:
            output['y_predicted_probabilities'] = {str(k): v for k, v in y_predicted_proba.items()}
        if y_predicted is not None:
            self.y_pred_list.append(y_predicted)
            
            output['y_predicted'] = y_predicted
        if self.metrics_list is not None and (y_predicted is not None or y_predicted_proba is not None) :
            output['metrics'] = latest_metrics

        output = _convert_numpy_types(output)

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
        The are 4 main cases: 

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
        
        4. The model has an update method
        
        This is for drift detection algorithms. Because there is no y_predicted we return the index of the value that
        drift was detected and we plot it on a scatter plot. 
        
        """
        
        y_predicted, y_predicted_proba = None, None
        
        if hasattr(self.model, "predict_one"):
            y_predicted = self.model.predict_one(X)
            #print(y_predicted)
            #print(y_predicted)
            # For probabilistic metrics
            if self.metrics_list and self.metrics['probabilistic'] is not None:
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
                
        elif hasattr(self.model, "update"):
            value = next(iter(X.values()))
            self.model.update(value) 
            if self.model.drift_detected: 
                y_predicted = next(iter(X))
                
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
                    #print(y , y_predicted)
                    
                    #print(y , y_predicted)
                    
                    metrics_in_group.update(y, y_predicted)
                    #print(metrics_in_group.update(y, y_predicted))
                    #print(metrics_in_group.update(y, y_predicted))

        # Store the metrics values
        for metric in self.metrics_list:
            metric_name = metric.__class__.__name__
            latest_value = metric.get()
            self.metrics_values[metric_name].append(latest_value)
            latest_metrics[metric_name] = latest_value
        #print(latest_metrics)
        #print(latest_metrics)
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
        #print(self.metrics_values)
        if self.metrics_list is not None: 
            for metric_name, values in self.metrics_values.items():
                
                fig.add_trace(go.Scatter(
                    y=values,
                    mode="lines",
                    name=f"{self.name} - {metric_name}",
                    #hoverinfo="y+name",
                    hovertemplate=f"{self.name} - {metric_name}"+"<br>Value:%{y}<br>Iteration:%{x}<extra></extra>"
                ), row=row, col=col)
            
    def add_stats_traces(self,traces): #fig, row=1, col=1) : 
        if type(self.model) == RiverPipeline:
            model_instance = self.model[self.model_name]
        else:
            model_instance = self.model
        
        if issubclass(type(model_instance), base.Classifier):
            #print(model_instance)
            y_true = np.array(self.y_true_list)
            y_pred = np.array(self.y_pred_list)
            # Get unique labels for axes
            labels = sorted(set(y_true) | set(y_pred))
            cm = confusion_matrix(self.y_true_list, self.y_pred_list)
            traces.append(go.Heatmap(
                        z = cm,
                        x=labels,  # predicted
                        y=labels,  # true
                        colorscale='Viridis',
                        name=f"{self.name} Predictions",
                        colorbar=dict(
                            title='Count',
                            #len=0.5,  # 50% of the plot height
                            #xanchor='left'
                            ),
                        hovertemplate='True: %{y}<br>Predicted: %{x}<br>Count: %{z}<extra></extra>'
    
                )
            )
            
        elif issubclass(type(model_instance) , base.Regressor) : 
            #print(model_instance)
            #print(self.y_true_list)
            #print(self.y_pred_list)
            traces.append(go.Scatter(
                        x=self.y_true_list,
                        y=self.y_pred_list,
                        mode='markers',
                        #marker=dict(color='blue', size=6, opacity=0.7),
                        name=f"{self.name} Predictions",
                        hovertemplate='True: %{x}<br>Predicted: %{y}<extra></extra>'
                )#, row=row, col=col
            )
            # Optionally, add a y=x reference line
            min_val = min(np.min(self.y_true_list), np.min(self.y_pred_list))
            max_val = max(np.max(self.y_true_list), np.max(self.y_pred_list))
            #print(min_val)
            traces.append(
                go.Scatter(
                    x=[min_val, max_val],
                    y=[min_val, max_val],
                    mode='lines',
                    line=dict(color='red', dash='dash'),
                    name='Ideal: y = x',
                    showlegend=True
                ),
                #row=row, col=col
            )
        elif issubclass(type(model_instance), base.Clusterer):
            # Count occurrences of each cluster label in y_pred_list
            cluster_counts = Counter(self.y_pred_list)
            print(self.y_pred_list)
            clusters = list(cluster_counts.keys())
            #print(cluster_counts)
            counts = list(cluster_counts.values())

            traces.append(
                go.Bar(
                    x=clusters,
                    y=counts,
                    name=f"{self.name} Cluster Counts",
                    #marker=dict(color='orange'),
                    hovertemplate='Cluster: %{x}<br>Count: %{y}<extra></extra>'
                )
            )
        elif issubclass(type(model_instance), base.DriftDetector):  
            
            traces.append(
                go.Scatter(
                    x=self.y_pred_list,
                    mode='markers',
                    #marker=dict(color='red', size=10, symbol='x'),
                    name='Drift Detected',
                    hovertemplate='Drift detected at index: %{x}<extra></extra>'
                )
            )
            
        else : 
            StatisticsWarning()
            


def _convert_numpy_types(obj):
    if isinstance(obj, dict):
        return {k: _convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_convert_numpy_types(v) for v in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj