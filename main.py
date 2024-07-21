import deliberating_agent as da
from datetime import datetime
import csv

cases = []

with open('sample_data.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for index, row in enumerate(spamreader):
        if index == 0:
            continue
        cases.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]])

results = [['ID', 'Datetime', 'Latitude', 'Longitude', 'Temperature (Cº)', 'Wind Speed (Km/H)', 'Humidity (%)', 'Risk factor', 'Surroundings', 'Expected decisions', 'Given decisions']]

for case in cases:
    drone_data = {
        "risk_factor": case[7],
        "surroundings": case[8],
        "location": [float(case[2]), float(case[3])],
        "datetime": datetime.strptime(case[1], "%d/%m/%Y %H:%M:%S")
        }
    weather_data = {
        "temperature": int(case[4]),
        "wind_speed": int(case[5]),
        "humidity": int(case[6])
        }

    # Evaluate situation and make decisions
    situation = da.evaluate_situation(drone_data, weather_data)
    expected_decisions = da.make_decisions(situation)
    given_decisions = da.make_decisions(situation, True)
    results.append([case[0], case[1], case[2], case[3], case[4], case[5], case[6], case[7], case[8], expected_decisions, given_decisions])

with open('results.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in results:
        spamwriter.writerow(row)

print('Results written in results.csv')