# %%

import matplotlib.pyplot as plt
import datetime as dt
from river import datasets
from river import time_series
from river import utils

period = 12
model = time_series.SNARIMAX(
    p=period,
    d=1,
    q=period,
    m=period,
    sd=1
)

for t, (x, y) in enumerate(datasets.AirlinePassengers()):
    model.learn_one(y)

horizon = 12
future = [
    {'month': dt.date(year=1961, month=m, day=1)}
    for m in range(1, horizon + 1)
]
forecast = model.forecast(horizon=horizon)
for x, y_pred in zip(future, forecast):
    print(x['month'], f'{y_pred:.3f}')
# %%
datasets.AirlinePassengers()
# %%
dataset = datasets.AirlinePassengers()

future_dates = [x['month'] for x in future]


# Extract data for plotting
dates = []
passengers = []
for x, y in dataset:
    dates.append(x['month'])
    passengers.append(y)


# Plot the data
plt.figure(figsize=(10, 5))
plt.plot(dates, passengers, label='Number of Passengers')
plt.plot(future_dates, forecast, 'r--', label='Forecasted Passengers')


plt.xlabel('Date')
plt.ylabel('Number of Passengers')
plt.title('Airline Passengers Over Time')
plt.legend()
plt.show()

# %%
