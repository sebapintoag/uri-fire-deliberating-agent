# type: object, activity, weather, fire
# This function always evaluates weather data. If drone data is received, it considers most recent weather data
#   and they're evaluated togheter.
def evaluate_situation(drone_data={}, weather_data={}):
    DANGEROUS_OBJECTS = [
        "trash",
        "dry_grass",
        "wood",
        "electric_cables",
        "gas_installation",
    ]
    DANGEROUS_ACTIVITIES = [
        "smoking",
        "bonfire",
        "bbq",
        "burning_trash",
        "suspicious_presence",
        "soldering",
    ]
    VULNERABLE_SURROUNDINGS = ["grass", "trees", "trash", "houses"]

    risk_rank = 5
    drone_data_type = None

    #breakpoint()

    # Evaluate dron data
    if drone_data and drone_data.get("risk_factor") == "fire":
        return {"type": "fire", "risk_rank": 0, "location": drone_data.get("location")}

    if drone_data and drone_data.get("risk_factor") in DANGEROUS_OBJECTS:
        drone_data_type = "object"
        risk_rank -= 1
        if drone_data.get("surroundings") in VULNERABLE_SURROUNDINGS:
            risk_rank -= 1
    elif drone_data and drone_data["risk_factor"] in DANGEROUS_ACTIVITIES:
        drone_data_type = "activity"
        risk_rank -= 1
        if drone_data.get("surroundings") in VULNERABLE_SURROUNDINGS:
            risk_rank -= 1

    # Evaluate weather data
    if weather_data["temperature"] >= 30.0:
        risk_rank -= 1
    if weather_data["wind_speed"] >= 30.0:
        risk_rank -= 1
    if weather_data["humidity"] <= 5.0:
        risk_rank -= 1

    if drone_data and len(drone_data) > 0:
        return {
            "type": drone_data_type,
            "subtype": drone_data["risk_factor"],
            "risk_rank": risk_rank,
            "location": drone_data.get("location"),
        }

    return {
        "type": "weather",
        "subtype": "trash",
        "risk_rank": risk_rank,
        "place": weather_data["place"],
    }


# type: call, monitoring_proposal
def make_decisions(situation_state):
    decisions = []

    if situation_state["type"] == "fire":
        decisions.append(
            {"type": "call", "collaborator": "fire_fighters", "location": situation_state.get("location")}
        )

    if situation_state["type"] == "weather" and situation_state.get("risk_rank") <= 3:
        decisions.append(
            {"type": "monitoring_proposal", "place": situation_state["place"]}
        )

    if situation_state["type"] in ["object", "activity"]:
        if situation_state["subtype"] in ["trash", "wood", "dry_grass"]:
            decisions.append(
                {
                    "type": "call",
                    "collaborator": "trash_collectors",
                    "location": situation_state.get("location"),
                }
            )
        elif situation_state["subtype"] in ["electric_cables"]:
            decisions.append(
                {
                    "type": "call",
                    "collaborator": "electric_operators",
                    "location": situation_state.get("location"),
                }
            )
        elif situation_state["subtype"] in ["gas_installation"]:
            decisions.append(
                {
                    "type": "call",
                    "collaborator": "gas_operators",
                    "location": situation_state.get("location"),
                }
            )
        elif situation_state["subtype"] in ["bonfire", "burning_trash"]:
            decisions.append(
                {
                    "type": "call",
                    "collaborator": "security",
                    "location": situation_state.get("location"),
                }
            )
            decisions.append(
                {
                    "type": "call",
                    "collaborator": "fire_fighters",
                    "location": situation_state.get("location"),
                }
            )
        elif situation_state["subtype"] in [
            "smoking",
            "bbq",
            "suspicious_presence",
            "soldering",
        ]:
            decisions.append(
                {
                    "type": "call",
                    "collaborator": "security",
                    "location": situation_state.get("location"),
                }
            )
    # No mather what, if risk_rank is 2 or less and, government authorities are notified
    if situation_state["risk_rank"] <= 2 and situation_state["type"] != "weather":
        decisions.append(
            {
                "type": "call",
                "collaborator": "authorities",
                "location": situation_state.get("location"),
            }
        )

    return decisions
