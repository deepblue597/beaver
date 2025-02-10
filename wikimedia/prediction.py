# %%
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

# %%
# Load the trained model from the file
with open('HoeffdingTreeClassifier.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# %%
# New test data
test_event = {
    "domain": "commons.wikimedia.org",
    "namespace": "File",
    "title": "File:Veloren-0.17-screenshot-sunset.jpg",
    "comment": "Removing template; rename done",
    "user_name": "Wieralee",
    "minor": False,
    "old_length": 3690,
    "new_length": 3561,
    "len_diff": 3690 - 3561
}

y = {"user_type": "human", }  # Target label for testing purposes

# Get the true label (for testing purposes)
true_label = 1 if y["user_type"] == "bot" else 0  # 1 for bot, 0 for human
# %%
# Make prediction with the trained model
predicted_class = model.predict_one(test_event)

# Print results
print(f"True label: {'bot' if true_label == 1 else 'human'}")
print(f"Predicted: {'bot' if predicted_class == 1 else 'human'}")

# %%
