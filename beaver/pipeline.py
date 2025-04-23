#TODO: Create a pipeline class 
import dill

class Pipeline:
    def __init__(self, model, metrics : list, name : str ,  output_topic : str = None ):
        self.model = model
        self.output_topic = output_topic
        self.metrics = metrics
        self.name = name
        for metric in self.metrics:
            metric.n 

        
    def train_and_predict(self, X , y : str = None) -> dict:
        pass 
        y = X[y]
        X = {key: value for key, value in X.items() if key != self.y}
        
        # Train the model
        self.model.learn_one(X, y)
        
        # Predict the class
        y_predicted = self.model.predict_one(X)
        
        # Update metrics
        self.metrics.update(y, y_predicted)

        with open(f'{self.name}.pkl', 'wb') as model_file:
            dill.dump(self.model, model_file)

        return { 
            **X, 
            
        }