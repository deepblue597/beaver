# %%
import requests
import matplotlib.pyplot as plt

# %%
response = requests.get(
    "https://api.electricitymap.org/v3/carbon-intensity/latest?zone=FR",
    headers={
        "auth-token": f"cVbydpxzZLhtoYbTsaaV"
    }
)
print(response.json())

# %%
response = requests.get(
    "https://api.electricitymap.org/v3/power-breakdown/latest?zone=FR",
    headers={
        "auth-token": f"cVbydpxzZLhtoYbTsaaV"
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

# %%
