#TODO: Create a pipeline class 
import dill

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
    def __init__(self, model, metrics : list, name : str ,  output_topic : str = None ):
        self.model = model
        self.output_topic = output_topic
        self.metrics = metrics
        self.name = name
        self.metrics_values = {metric.__class__.__name__: [] for metric in metrics}
            

    def __str__(self):
        return f"Pipeline: {self.name}, Model: {self.model}, Metrics: {self.metrics}, Output Topic: {self.output_topic}"
    
    def train_and_predict(self, X , y : str = None) -> dict:
        """
        Train the model on the input data and make predictions.
        Add the values of metrics into a list and return a dict containing the 
        input data the prediction and the metrics values.
        """
        y = X[y]
        X = {key: value for key, value in X.items() if key != self.y}
        
        # Train the model
        self.model.learn_one(X, y)
        
        # Predict the class
        y_predicted = self.model.predict_one(X)
        
        # Update metrics
        self.metrics.update(y, y_predicted)

        # Store the metrics values
        for metric in self.metrics:
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