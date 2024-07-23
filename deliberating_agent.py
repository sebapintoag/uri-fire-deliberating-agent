import random

DANGEROUS_ACTIVITIES = ['smoking', 'lit campfire', 'lighting a grill', 'burning waste', 'suspicious presence', 'soldering']
DANGEROUS_ELEMENTS = ['wastes', 'dry grass', 'wood', 'papers', 'illegal electricity connection', 'gas recipient', 'glass', 'glass bottle', 'bonfire', 'grill on', 'fire', 'smoke']
VULNERABLE_SURROUNDINGS = ['grass', 'dry grass', 'trees', 'trash', 'house', 'tent', 'electric connection', 'fuel recipient', 'wood']

DECISIONS_HISTORY = {}

def evaluate_situation(drone_data={}, weather_data={}):
    # Risk score
    score = 0
    # Weather data
    temperature = weather_data['temperature']
    wind_speed = weather_data['wind_speed']
    humidity = weather_data['humidity']
    # Drone data
    risk_factor = drone_data['risk_factor']
    surroundings = drone_data['surroundings']
    distance = drone_data['distance']
    lat = drone_data['location'][0]
    lng = drone_data['location'][1]
    datetime = drone_data['datetime']
    # Danger detections
    fire_danger = False
    weather_danger = False
    element_danger = False
    activity_danger = False
    surroundings_danger = False
    previous_danger = False

    close_distance = False

    # Evaluate weather data
    if temperature >= 30:
        score = score + 1
    if wind_speed >= 30:
        score = score + 1
    if humidity <= 30:
        score = score + 1
    if score == 3:
        weather_danger = True

    # Evaluate distance between risk_factor and detected surroundings
    if distance < 50:
        score = score + 3
        close_distance = True
    elif distance < 100:
        score = score + 2
        close_distance = True
    elif distance < 250:
        score = score + 1

    # Evaluate dron data
    if risk_factor in ['fire', 'smoke']:
        # Should call emergency services right away or assign highest score
        fire_danger = True
        score = score + 12
        if surroundings in VULNERABLE_SURROUNDINGS:
            surroundings_danger = True
    if risk_factor != 'none':
        if risk_factor in DANGEROUS_ACTIVITIES:
            activity_danger = True
            if surroundings in VULNERABLE_SURROUNDINGS:
                surroundings_danger = True
                if weather_danger:
                    score = score + 5 # Max: 8
                else:
                    score = score + 3 # Max: 5
            else:
                if weather_danger:
                    score = score + 4 # Max: 7
                else:
                    score = score + 2 # Max: 4
        elif risk_factor in DANGEROUS_ELEMENTS:
            element_danger = True
            if surroundings in VULNERABLE_SURROUNDINGS:
                surroundings_danger = True
                if weather_danger:
                    score = score + 3 # Max: 6
                else:
                    score = score + 2 # Max: 4
            else:
                if weather_danger:
                    score = score + 2 # Max: 5
                else:
                    score = score + 1 # Max: 2

    # TODO: Evaluate past data in same or near location

    return {
        'score': score,
        'risk_factor': risk_factor,
        'fire_danger': fire_danger,
        'weather_danger': weather_danger,
        'activity_danger': activity_danger,
        'element_danger': element_danger,
        'surroundings_danger': surroundings_danger,
        'close_distance': close_distance,
        'previous_danger': previous_danger,
        'lat': lat,
        'lng': lng,
        'datetime': datetime  }

def make_decisions(situation_state):
    score = situation_state['score']
    risk_factor = situation_state['risk_factor']
    fire_danger = situation_state['fire_danger']
    weather_danger = situation_state['weather_danger']
    activity_danger = situation_state['activity_danger']
    element_danger = situation_state['element_danger']
    surroundings_danger = situation_state['surroundings_danger']
    close_distance = situation_state['close_distance']
    previous_danger = situation_state['previous_danger']
    lat = situation_state['lat']
    lng = situation_state['lng']
    datetime = situation_state['datetime']

    decisions = []

    if fire_danger:
        decisions.append("Call fire fighters")
        decisions.append("Notify government authorities")
        if surroundings_danger:
            decisions.append('Notify local authorities')
            decisions.append('Evacuate zone')

    if score >= 12:
        decisions.append('Request support to security forces')
        if surroundings_danger or close_distance:
            decisions.append('Notify local collaborators')
    if score >= 9:
        if activity_danger:
            decisions.append('Request support to security forces')
            decisions.append("Notify government authorities")
            decisions.append('Notify local authorities')
            if surroundings_danger or close_distance:
                decisions.append('Notify local collaborators')
        elif element_danger:
            if surroundings_danger or close_distance or risk_factor in ['gas recipient', 'bonfire', 'grill on']:
                decisions.append('Notify local authorities')
            if risk_factor in ['wastes', 'wood', 'papers', 'glass', 'glass bottle']:
                decisions.append('Contact waste collectors')
            elif risk_factor in ['illegal electricity connection']:
                decisions.append('Notify power company')
            elif risk_factor in ['bonfire']:
                decisions.append('Call fire fighters')
            else:
                decisions.append('Notify local collaborators')
    if score >= 6:
        if activity_danger:
            decisions.append('Request support to security forces')
            decisions.append("Notify government authorities")
            decisions.append('Notify local authorities')
            if surroundings_danger:
                decisions.append('Notify local collaborators')
        elif element_danger:
            if close_distance and (surroundings_danger or risk_factor in ['bonfire', 'grill on']):
                decisions.append('Notify local authorities')
            if risk_factor in ['wastes', 'wood', 'papers', 'glass', 'glass bottle']:
                decisions.append('Contact waste collectors')
            elif risk_factor in ['illegal electricity connection']:
                decisions.append('Notify power company')
            elif risk_factor in ['bonfire']:
                decisions.append('Call fire fighters')
            if close_distance:
                decisions.append('Notify local collaborators')
    elif score >= 3:
        if activity_danger:
            decisions.append('Notify local authorities')
            if surroundings_danger and close_distance:
                decisions.append('Notify local collaborators')
        elif element_danger:
            if surroundings_danger and close_distance:
                decisions.append('Notify local collaborators')
            if risk_factor in ['wastes', 'papers', 'glass', 'glass bottle']:
                decisions.append('Contact waste collectors')
            elif risk_factor in ['bonfire']:
                decisions.append('Call fire fighters')
        else:
            decisions.append('Propose monitoring flight')
    else:
        if weather_danger:
            decisions.append('Propose monitoring flight')
        if activity_danger:
            decisions.append('Notify local authorities')
        if (surroundings_danger or element_danger) and close_distance:
            decisions.append('Notify local collaborators')

    # TODO: Store decisions made

    return decisions
