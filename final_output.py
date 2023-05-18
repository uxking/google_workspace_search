# open a json file
import json
import csv

with open("google_workspace_apps/output.json", "r") as file:
    data = json.load(file)

# output data as a csv
with open("google_workspace_apps/final_output.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "link"], delimiter="#")
    writer.writeheader()
    writer.writerows(data)
