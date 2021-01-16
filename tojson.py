import json
import csv

with open("Pythontest.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    data = []
    for row in reader:
        data.append({"name": row[0], "sites": row[1], "host-address": row[2]})

with open("names.json", "w") as f:
    json.dump(data, f, indent=4)