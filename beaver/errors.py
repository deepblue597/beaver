import logging

class PredictionWarning(Warning):
    """Custom warning logged when the model fails to make predictions."""
    def __init__(self, message="Both y_predicted and y_predicted_proba are None."):
        self.message = message
        #TODO: Create custom logger
        logging.getLogger("quixstreams").warning(self.message)
        super().__init__(self.message)


class StatisticsWarning(Warning):
    """Custom warning logged when the model fails to make statistics."""
    def __init__(self, message="Statistics are not available for this model."):
        self.message = message
        #TODO: Create custom logger
        logging.getLogger("quixstreams").warning(self.message)
        super().__init__(self.message)