# %%
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt


# %%
# Load the trained model from the file
with open('SNARIMAX_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# %%
horizon = 12
future = [
    {'month': dt.date(year=2025, month=m, day=1)}
    for m in range(1, horizon + 1)
]

# %%
forecast = model.forecast(horizon=horizon)
for x, y_pred in zip(future, forecast):
    print(x['month'], f'{y_pred:.3f}')

# %%
future_dates = [x['month'] for x in future]

plt.figure(figsize=(10, 5))
# plt.plot(dates, carbon_intensity, label='Carbon Intensity (his)')
plt.plot(future_dates, forecast, 'r--', label='Forecasted Carbon Intensity')


plt.xlabel('Date')
plt.ylabel('Carbon Intensity (gCO2/kWh)')
plt.title('Carbon Intensity Over Time')
plt.legend()
plt.show()

# %%
