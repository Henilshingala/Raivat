import pandas as pd
import json

# Load CSV files
countries_df = pd.read_csv("countries.csv")
states_df = pd.read_csv("states.csv")
cities_df = pd.read_csv("cities.csv")

# Create a country code to full name + short code map
country_code_map = {
    row['iso2']: f"{row['name']} ({row['iso3']})"
    for _, row in countries_df.iterrows()
}

# Create a dictionary to hold final nested result
full_nested_data = {}

# Iterate over each unique country code in states
for country_code in states_df['country_code'].unique():
    country_label = country_code_map.get(country_code)
    if not country_label:
        continue

    # Filter states and cities for this country
    country_states = states_df[states_df['country_code'] == country_code]
    country_cities = cities_df[cities_df['country_code'] == country_code]

    # Store state-to-cities mapping here
    state_dict = {}

    for _, state in country_states.iterrows():
        state_name = state['name']
        state_code = state['state_code']

        if pd.isna(state_code) or pd.isna(state_name):
            continue

        state_label = f"{state_name} ({state_code})"

        # Get all cities under this state
        state_cities = country_cities[country_cities['state_code'] == state_code]['name'].dropna().tolist()
        if state_cities:
            state_dict[state_label] = state_cities

    # Only add country if it has valid states
    if state_dict:
        full_nested_data[country_label] = state_dict

# Export to JSON
with open("country_state_city_full.json", "w", encoding="utf-8") as f:
    json.dump(full_nested_data, f, ensure_ascii=False, indent=2)

print("✅ JSON saved as 'country_state_city_full.json'")
