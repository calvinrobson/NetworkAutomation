import json
import csv

with open("sites.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    data = []
    for row in reader:
        data.append({"name": row[0], "slug": row[1]})

with open("sites.json", "w") as f:
    json.dump(data, f, indent=4)

