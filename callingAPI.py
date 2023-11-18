import requests
import schedule
import time
import logging

logging.basicConfig(level=logging.ERROR)

def fetch_data_from_api():
    try:
        url = "https://premier-league-standings1.p.rapidapi.com/"
        headers = {
            "X-RapidAPI-Key": "2eb0ad9717msh5a898288a798d61p1803ffjsn8c47cfe397c2",
            "X-RapidAPI-Host": "premier-league-standings1.p.rapidapi.com",
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.text
        else:
            logging.error(f"Error during network request. Status code: {response.status_code}")
            return ""
    except Exception as e:
        logging.error("Error during network request", exc_info=True)
        return ""

def job():
    data = fetch_data_from_api()
    # Process the data as needed
    print(data)

# Run the job every 30 minutes
schedule.every(30).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)