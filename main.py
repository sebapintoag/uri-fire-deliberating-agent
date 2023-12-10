import deliberating_agent as da
import printer

# Inputs
cases = [
    {
        "drone_data": {
            "risk_factor": "trash",
            "surroundings": "dry_grass",
            "location": [-33.051876, -71.547227],
        },
        "weather_data": {
            "temperature": 29.0,
            "wind_speed": 10.0,
            "humidity": 0.8,
            "place": "Valparaiso",
        },
    },
    {
        "drone_data": {
            "risk_factor": "smoking",
            "surroundings": "trash",
            "location": [-33.051876, -71.547227],
        },
        "weather_data": {
            "temperature": 20.0,
            "wind_speed": 26.0,
            "humidity": 20.2,
            "place": "Valparaiso",
        },
    },
    {
        "weather_data": {
            "temperature": 35.0,
            "wind_speed": 40.0,
            "humidity": 1.0,
            "place": "Valparaiso",
        },
    },
    {
        "drone_data": {
            "risk_factor": "fire",
            "surroundings": "houses",
            "location": [-33.051876, -71.547227],
        },
        "weather_data": {
            "temperature": 31.0,
            "wind_speed": 26.0,
            "humidity": 0.5,
            "place": "Valparaiso",
        },
    },
]

for i, case in enumerate(cases):
    drone_data = case.get("drone_data")
    weather_data = case.get("weather_data")

    print("-- Case " + str(i + 1) + " --")

    # Evaluate situation and make decisions
    situation = da.evaluate_situation(drone_data, weather_data)
    decisions = da.make_decisions(situation)


    # Print inputs and output
    printer.print_inputs(drone_data, weather_data)
    printer.print_output(decisions)
