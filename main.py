import csv
import re
from time import sleep
import requests
import json


# open a csv file and import the first column into an array called data
def import_data(filename) -> dict:
    data = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row[0])
    return data


# parse each data value, up to but not including a certain character
def parse_data(data) -> dict:
    parsed_data = []
    for value in data:
        parsed_data.append(re.split("-|\.", value)[0])
        # parsed_data.append(value.split("-" | ".")[0])
    return parsed_data


# function takes an a list and outputs it to a file
def write_file(data) -> None:
    with open("google_workspace_search/output.json", "w") as output:
        json.dump(data, output)


# function receives an dict and iterates over each value performing a search with google
def search_data(data) -> list:
    app_list = []
    for app_id in data:
        query = f"inurl:{app_id}"
        print(f"app id is {app_id}")
        print(f"query string is {query}")

        response = requests.get(URL + query + "&key=" + KEY)
        print(response.status_code)
        if response.status_code != 200:
            print("error")
            continue
        json_response = json.loads(response.text)
        results = int(json_response["searchInformation"]["totalResults"])
        if results > 0:
            print(f"app id {app_id} is a Marketplace App")
            app_data = {
                "title": json_response["items"][0]["title"],
                "link": json_response["items"][0]["link"],
            }
            app_list.append(app_data)
            # app_data.append(json_response["items"][0]["link"])
            # print(app_list)

        else:
            print(f"app id {app_id} is not a Marketplace App")

        sleep(1.677)
        # _ = input("Press enter to continue...")
    return app_list


# this is always the site to search
# We will be searchine "workspace.google.com" as configured by the Programmable Search Engine - no need to include in query

# Search Engine ID
SEID = "f748536010c774a1b"
URL = "https://customsearch.googleapis.com/customsearch/v1?c2coff=0&cx=f748536010c774a1b&filter=1&num=1&q="
KEY = "[yourkey]"  # this is safe to pass in the url per google.

apps = import_data("google_workspace_search/oauth_data.csv")

app_ids = parse_data(apps)
app_list_final = search_data(app_ids)
write_file(app_list_final)
