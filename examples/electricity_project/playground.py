# %%

import matplotlib.pyplot as plt
import datetime as dt
from river import datasets
from river import time_series
from river import utils
import pandas as pd

# %%

# List of CSV files
csv_files = ["FR_2021_hourly.csv", "FR_2022_hourly.csv",
             "FR_2023_hourly.csv", "FR_2024_hourly.csv"]

# Read and concatenate all CSVs
combined_df = pd.concat([pd.read_csv(file)
                        for file in csv_files], ignore_index=True)
# %%
# Save the combined CSV
combined_df.to_csv("combined_file_hourly.csv", index=False)

print("Files successfully combined!")
# %%
# Extract Datetime and Carbon Intensity values
dates = combined_df['Datetime (UTC)']
carbon_intensity = combined_df['Carbon Intensity gCO₂eq/kWh (direct)'].astype(
    float)
# %%

# Plot the data
plt.figure(figsize=(10, 5))
plt.plot(dates, carbon_intensity, label='Carbon Intensity')
plt.xlabel('Date')
plt.ylabel('Carbon Intensity (gCO2/kWh)')
plt.title('Carbon Intensity Over Time')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# %%
period = 12
model = time_series.SNARIMAX(
    p=period,
    d=1,
    q=period,
)


# %%

# Train the model with the carbon intensity data
for t in carbon_intensity:
    model.learn_one(t)

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

# %%
dates = pd.to_datetime(dates)


plt.figure(figsize=(10, 5))
plt.plot(dates, carbon_intensity, label='Carbon Intensity (his)')
plt.plot(future_dates, forecast, 'r--', label='Forecasted Carbon Intensity')


plt.xlabel('Date')
plt.ylabel('Carbon Intensity (gCO2/kWh)')
plt.title('Carbon Intensity Over Time')
plt.legend()
plt.show()

# %%
