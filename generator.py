import random
import copy
import csv
from datetime import datetime, timedelta

# Sample data for each variable
SAMPLE_RISK_ACTIVITIES = ['smoking', 'lit campfire', 'lighting a grill', 'burning waste', 'suspicious presence', 'soldering', 'none']
SAMPLE_RISK_ELEMENTS = ['wastes', 'dry grass', 'wood', 'papers', 'illegal electricity connection', 'gas recipient', 'glass', 'glass bottle', 'bonfire', 'grill on', 'fire', 'smoke', 'none']
SAMPLE_SURROUNDINGS = ['grass', 'dry grass', 'ground', 'trees', 'trash', 'house', 'tent', 'electric connection', 'fuel recipient', 'wood', 'highway', 'road', 'street']
#SAMPLE_TEMPERATURE_VALUES = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70]
#SAMPLE_WIND_SPEED_VALUES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 123, 114, 115, 116, 117, 118, 119, 120]
#SAMPLE_HUMIDITY_VALUES = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]

SAMPLE_TEMPERATURE_VALUES = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
SAMPLE_WIND_SPEED_VALUES = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 123, 114, 115, 116, 117, 118, 119, 120]
SAMPLE_HUMIDITY_VALUES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]

# Moverse restando a latitud (ir hacia abajo) y sumando a longitud (ir hacia la derecha)
START_COORDINATES = {'lat': -33.045642, 'lng': -71.535046}
MINUTES_PER_DAY = 60 * 24
REGISTER_AT_MINUTES = 10 # Register data every 10 minutos
current_coordinates = copy.deepcopy(START_COORDINATES)
i = 0
aux_lng = 1
aux_lat = 1
data = [['ID', 'Datetime', 'Latitude', 'Longitude', 'Temperature (Cº)', 'Wind Speed (Km/H)', 'Humidity (%)', 'Risk factor', 'Surroundings']]
start_datetime = datetime(2023, 12, 1, 0, 0, 0)
temp_aux = random.choice(SAMPLE_TEMPERATURE_VALUES)
wind_speed_aux = random.choice(SAMPLE_WIND_SPEED_VALUES)
humidity_aux = random.choice(SAMPLE_HUMIDITY_VALUES)
while i < 15000:
    register = []
    # Set current datetime
    current_datetime = start_datetime + timedelta(minutes=REGISTER_AT_MINUTES * i)
    # Set temperature or increase it
    if i % 9 == 0:
        temp_aux = random.choice(SAMPLE_TEMPERATURE_VALUES)
    else:
        temp_aux = temp_aux + 1 * random.choice([-1, 0, 1])
    # Set wind speed or increase it
    if i % 5 == 0:
        wind_speed_aux = random.choice(SAMPLE_WIND_SPEED_VALUES)
    else:
        wind_speed_aux = wind_speed_aux + 3 * random.choice([-1, 0, 1])
    # Set humidity or decrease it
    if i % 12 == 0:
        humidity_aux = random.choice(SAMPLE_HUMIDITY_VALUES)
    else:
        humidity_aux = humidity_aux + 2 * random.choice([-1, 0, 1])
    # Move coordinates
    if ((i % (MINUTES_PER_DAY/REGISTER_AT_MINUTES)) == 0) or (i == 0):
        # At the start of a new day returns to origin and starts all over again
        current_coordinates = copy.deepcopy(START_COORDINATES)
        aux_lng = 1
        aux_lat = 1
    elif (i % 90) == 0:
        current_coordinates['lng'] = current_coordinates['lng'] + aux_lng * 0.005000
        aux_lat = aux_lat * -1
    elif (i % 10) == 0:
        current_coordinates['lat'] = current_coordinates['lat'] - aux_lat * 0.005000
        aux_lng = aux_lng * -1
    else:
        current_coordinates['lng'] = current_coordinates['lng'] + aux_lng * 0.005000
    # Select risk factor
    risk_factor = random.choice(SAMPLE_RISK_ELEMENTS + SAMPLE_RISK_ACTIVITIES)
    # Select surrounding
    surrounding = random.choice(SAMPLE_SURROUNDINGS)
    # Add data
    data.append([i, current_datetime.strftime("%d/%m/%Y %H:%M:%S"),
                 current_coordinates['lat'], current_coordinates['lng'],
                 temp_aux, wind_speed_aux, humidity_aux,
                 risk_factor, surrounding])
    i = i + 1

with open('sample_data.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in data:
        spamwriter.writerow(row)