# %%
from datetime import datetime, timedelta
from river import utils
from river import time_series
from river import datasets
import datetime as dt
import csv
import requests
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
# %% Load the necessary tokens

load_dotenv()

ELEC_TOKEN = os.getenv('ELECTRICITY_TOKEN')

# %% Load latest data
response = requests.get(
    "https://api.electricitymap.org/v3/carbon-intensity/latest?zone=FR",
    headers={
        "auth-token": ELEC_TOKEN
    }
)
print(response.json())

# %% Electricity breakdown of France ( Consumption and Production )
response = requests.get(
    "https://api.electricitymap.org/v3/power-breakdown/latest?zone=FR",
    headers={
        "auth-token": ELEC_TOKEN
    }
)
print(response.json())

if response.status_code == 200:
    data = response.json()
    print(data)

    # Extract data for plotting
    consumption = data['powerConsumptionBreakdown']
    production = data['powerProductionBreakdown']

    # Filter out None values from production data
    cleaned_production = {k: v for k, v in production.items() if v is not None}
    cleaned_consumption = {k: v for k,
                           v in consumption.items() if v is not None}

    # Plot power consumption breakdown
    plt.figure(figsize=(10, 5))
    plt.bar(cleaned_consumption.keys(),
            cleaned_consumption.values(), color='blue')
    plt.xlabel('Energy Source')
    plt.ylabel('Power Consumption (MW)')
    plt.title('Power Consumption Breakdown')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Plot power production breakdown
    plt.figure(figsize=(10, 5))
    plt.bar(cleaned_production.keys(),
            cleaned_production.values(), color='green')
    plt.xlabel('Energy Source')
    plt.ylabel('Power Production (MW)')
    plt.title('Power Production Breakdown')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# %% Load historical data

response = requests.get(
    "https://api.electricitymap.org/v3/carbon-intensity/history?zone=FR",
    headers={
        "auth-token": ELEC_TOKEN
    }
)
print(response.json())
# %%

""" Predict the carbon intensity for the next X days """


# Define the path to your CSV file
csv_file_path = 'FR_2024_daily.csv'

# Read the CSV file and convert it to a list of dictionaries
data = []
with open(csv_file_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        data.append(row)

# Print the first few rows to verify
for row in data[:5]:
    print(row)

# %%
# Extract data for plotting
dates = [row['Datetime (UTC)'] for row in data]
carbon_intensity = [
    float(row['Carbon Intensity gCO₂eq/kWh (direct)']) for row in data]

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
# Convert dates and carbon intensity to a dictionary
carbon_intensity_dict = {date: ci for date, ci in zip(dates, carbon_intensity)}

# Print the first few entries to verify
for date, ci in list(carbon_intensity_dict.items())[:5]:
    print(date, ci)
# %%
period = 365
model = time_series.SNARIMAX(
    p=period,
    d=1,
    q=period,
    m=period,
    sd=1
)

for t, (x, y) in enumerate(carbon_intensity_dict.items()):
    model.learn_one(y)

# %%
# Generate future dates for the next 30 days
last_date = dates[-1]

# %%
last_date = datetime.strptime(last_date, "%Y-%m-%d %H:%M:%S")


# %%

horizon = 60
future = [{'date': (last_date + timedelta(days=i)).date()}
          for i in range(1, horizon + 1)]

# %%
# Forecast the next 30 days

forecast = model.forecast(horizon=horizon)

# Print the forecasted values
for x, y_pred in zip(future, forecast):
    print(x['date'], f'{y_pred:.3f}')
# %%


future_dates = [x['date'] for x in future]
# %%
# Plot the data
plt.figure(figsize=(10, 5))
# plt.plot(dates, carbon_intensity, label='Number of Passengers')
plt.plot(future_dates, forecast, 'r--', label='Forecasted Passengers')


plt.xlabel('Date')
plt.ylabel('Number of Passengers')
plt.title('Airline Passengers Over Time')
plt.legend()
plt.show()

# %%
dates = [row['Datetime (UTC)'] for row in data][:30]
carbon_intensity = [
    float(row['Carbon Intensity gCO₂eq/kWh (direct)']) for row in data][:30]


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
