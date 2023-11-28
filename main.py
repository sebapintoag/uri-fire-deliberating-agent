import deliberating_agent as da

# Inputs
drone_data = {
    'risk_factor': 'trash',
    'surroundings': 'dry_grass',
    'location': [-33.051876, -71.547227],
}

weather_data = {
    'temperature': 29.0,
    'wind_speed': 30.0,
    'humidity': 0.8,
    'place': 'Valparaiso'
}

situation = da.evaluate_situation(drone_data, weather_data)
decisions = da.make_decisions(situation)

print(decisions)