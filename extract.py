import requests 
from config import TFL_API_URL

def extract():
    response = requests.get(TFL_API_URL)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    data = extract()
    for line in data:
        print(line["name"], "-", line["lineStatuses"][0]["statusSeverityDescription"])