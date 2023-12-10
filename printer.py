def print_inputs(drone_data, weather_data):
    print("\n\t-> Input data")
    if drone_data:
        print("\tDrone data:")
        print("\t- Risk factor: " + drone_data.get("risk_factor"))
        print("\t- Surroundings: " + drone_data.get("surroundings"))
    
    if weather_data:
        print("\tWeather data:")
        print("\t- Temperature: " + str(weather_data.get("temperature")))
        print("\t- Wind speed: " + str(weather_data.get("wind_speed")))
        print("\t- Humidity: " + str(weather_data.get("humidity")))

def print_output(decisions):
    print("\n\t-> Results")
    output = ""
    for decision in decisions:
        if decision.get("type") == "call":
            output = output + "Call to " + decision.get("collaborator").replace("_", " ") + "\n"
        elif decision.get("type") == "monitoring_proposal":
            output = output + "Propose a monitoring flight\n"
    print(output)
    