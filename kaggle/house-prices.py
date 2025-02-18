# %%
from river import datasets, preprocessing
import kagglehub
import pandas as pd
import os
from river import linear_model, metrics, datasets
import matplotlib.pyplot as plt
from river import stream
from sklearn.model_selection import train_test_split
import neptune
import os
from dotenv import load_dotenv
# %% Load the necessary tokens

load_dotenv()

NEPTUNE_TOKEN = os.getenv('NEPTUNE_TOKEN')

# %%
# Download latest version
path = kagglehub.dataset_download("fedesoriano/the-boston-houseprice-data")

print("Path to dataset files:", path)

# %%
csv_path = os.path.join(path, "boston.csv")

df = pd.read_csv(csv_path)

# %%
y = df.pop("MEDV")
# %%

X_train, X_test, y_train, y_test = train_test_split(
    df, y, test_size=0.2, random_state=42)


# %%
# Define the Passive-Aggressive Regressor model
model = (
    preprocessing.StandardScaler() |
    linear_model.LinearRegression(intercept_lr=.1)
)

# Define the evaluation metric (e.g., Mean Absolute Error)
metric = metrics.MAE()

# %% Iinitalize neptune

run = neptune.init_run(
    project="jason-k/boston-pricses",
    api_token=NEPTUNE_TOKEN,
)

# %%
# Log for LinearRegression in Neptune
run['model/hyperparameters'] = {
    'model': 'LinearRegression',  # Model type
    'intercept_lr': 0.1,          # Learning rate for the intercept
}

# %%
mae_values = []

# Train and evaluate the model
for xi, yi in stream.iter_pandas(X_train, y_train):
    y_predi = model.predict_one(xi)  # Predict the value
    metric.update(yi, y_predi)       # Update the metric
    model.learn_one(xi, yi)          # Update the model
    # Log the MAE metric at each iteration
    run['metrics/mae'].log(metric.get())
    mae_values.append(metric.get())
# Print the final MAE
print(metric.get())

# %%
# Plot the MAE over time
plt.plot(mae_values)
plt.xlabel('Iterations')
plt.ylabel('Mean Absolute Error (MAE)')
plt.title('MAE over Training Iterations')
plt.show()

# End the Neptune run when done
run.stop()
# %%
# Evaluate the model on the test data
for xi, yi in stream.iter_pandas(X_test, y_test):
    y_predi = model.predict_one(xi)  # Predict the value
    metric.update(yi, y_predi)       # Update the metric


# Print the final MAE (or any other metric you are using)
print("Test Set Evaluation MAE:", metric.get())

# %%
x_test = X_test.iloc[0]
y_t = y_test.iloc[0]
report = model.debug_one(x_test)
print(report)

# %%
y_test.iloc[0]
# %%
