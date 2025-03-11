# %%
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from datetime import datetime, timedelta
import dill


# %%
# Load the trained model from the file
with open('SNARIMAX_electricity_h.pkl', 'rb') as model_file:
    model = dill.load(model_file)
model.__dict__
# %% set the prediction horizon
horizon = 60
start_date = datetime(year=2025, month=1, day=1)

future = [{'hour': (start_date + timedelta(hours=i)
                    ).strftime("%Y-%m-%d %H:%M:%S")} for i in range(horizon)]

print(future)

# %% predict method
forecast = model.forecast(horizon=horizon)
for y_pred in forecast:
    print(f'{y_pred:.3f}')

# %%
future_dates = [x['hour'] for x in future]
# %%
combined_df = pd.read_csv('combined_file_hourly.csv')
dates = combined_df['Datetime (UTC)']
carbon_intensity = combined_df['Carbon Intensity gCO₂eq/kWh (direct)'].astype(
    float)

dates = pd.to_datetime(dates)

# %% plot the data (cannot be plotted for both hist and pred data)
plt.figure(figsize=(10, 5))
# plt.plot(dates, carbon_intensity, label='Carbon Intensity (his)')
plt.plot(future_dates, forecast, 'r--', label='Forecasted Carbon Intensity')


plt.xlabel('Date')
plt.ylabel('Carbon Intensity (gCO2/kWh)')
plt.title('Carbon Intensity Over Time')
plt.legend()
plt.show()
