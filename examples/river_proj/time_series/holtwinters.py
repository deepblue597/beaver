# %%
from collections import deque
import statistics
from river import metrics
from river import time_series, datasets
import datetime as dt
import matplotlib.pyplot as plt
from collections import deque

# Load the AirlinePassengers dataset
dataset = datasets.AirlinePassengers()
horizon = 12
# Initialize the Holt-Winters model with monthly seasonality (m=12)
# model = time_series.HoltWinters(
#     alpha=0.3,
#     beta=0.1,
#     gamma=0.6,
#     seasonality=12,
#     multiplicative=True
# )

period = 12
model = time_series.SNARIMAX(
    p=period,
    d=1,
    q=period,
    m=period,
    sd=1
)
y_pred_queue = deque(maxlen=2)
metric = metrics.MAE()
# Train the model on the dataset
for t, (x, y) in enumerate(datasets.AirlinePassengers()):
    model.learn_one(x=x, y=y)
    # model.forecast(horizon=1)
    # metric.update(y, model.forecast(horizon=1)[0])
    if t > model.m:
        # print('y', y)
        y_pred_queue.append(model.forecast(horizon=1)[0])
        # print(y_pred[-1][0])
    if t > model.m + 1:
        y_pred = y_pred_queue.popleft()
        metric.update(y, y_pred)
        print(metric)
        # time_series.evaluate((x, y), model, horizon=12, metric=metric)

# %%
# Forecast the next 12 months (next year)
forecast = [model.forecast(horizon=k) for k in range(1, horizon+1)]

print("Forecast for next year:", forecast)

# %%
metric = metrics.MAE()

steps = time_series.iter_evaluate(
    dataset,
    model,
    horizon=12,
    metric=metric
)

# Process the results step by step
for x, y, y_pred, horizon_metric in steps:
    print(
        f"Input: {x}, True: {y}, Prediction: {y_pred}, Metric: {horizon_metric}")

# %%
mae = time_series.evaluate(
    dataset,
    model,
    horizon=12,
    metric=metric
)
mae

# %%
metric = time_series.evaluate(
    dataset=datasets.AirlinePassengers(),
    model=time_series.HoltWinters(alpha=0.1),
    metric=metrics.MAE(),
    agg_func=statistics.mean,
    horizon=4
)
metric
# %%

last = deque(dataset, maxlen=1)  # Keep only the last element
last_x, last_y = last[0]

# %%
horizon = 12
future = [
    {'month': dt.date(year=1961, month=m, day=1)}
    for m in range(1, horizon + 1)
]
# %%
last_date = last_x['month']

# Define the forecast horizon
horizon = 12

# Generate future dates starting from the last date
future_dates = [
    (last_date + dt.timedelta(days=30 * i)).replace(day=1)
    for i in range(1, horizon + 1)
]

# future_dates = [x['month'] for x in future]

dates = []
passengers = []
for x, y in dataset:
    dates.append(x['month'])
    passengers.append(y)


# Plot the data
plt.figure(figsize=(10, 5))
plt.plot(dates, passengers, label='Number of Passengers')
# forecast[-1] because forecast is a list of list which starts with 1 pred ( next mont) and goes till 12 predictions ( the whole year)
plt.plot(future_dates, forecast[-1], 'r--', label='Forecasted Passengers')


plt.xlabel('Date')
plt.ylabel('Number of Passengers')
plt.title('Airline Passengers Over Time')
plt.legend()
plt.show()

# %%
plt.figure(figsize=(10, 5))
plt.plot([k for k in range(1, horizon+1)], mae_val, label='Mae')
# forecast[-1] because forecast is a list of list which starts with 1 pred ( next mont) and goes till 12 predictions ( the whole year)
# plt.plot(future_dates, forecast[-1], 'r--', label='Forecasted Passengers')
plt.show()
# %%
