# %%
from river import time_series, datasets
import datetime as dt
import matplotlib.pyplot as plt


# Load the AirlinePassengers dataset
dataset = datasets.AirlinePassengers()

# Initialize the Holt-Winters model with monthly seasonality (m=12)
model = time_series.HoltWinters(
    alpha=0.3,
    beta=0.1,
    gamma=0.6,
    seasonality=12,
    multiplicative=True
)

# Train the model on the dataset
for t, (x, y) in enumerate(datasets.AirlinePassengers()):
    model.learn_one(y)

# Forecast the next 12 months (next year)
forecast = [model.forecast(horizon=k) for k in range(1, 13)]

print("Forecast for next year:", forecast)

# %%
horizon = 12
future = [
    {'month': dt.date(year=1961, month=m, day=1)}
    for m in range(1, horizon + 1)
]

future_dates = [x['month'] for x in future]

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
