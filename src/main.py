#!/usr/bin/env python3

import logging
import sys
import requests
import os
from datetime import datetime

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(levelname)s: %(message)s')


def do_get_request(url: str, headers: dict):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logging.info("GET request successful: %s", response.status_code)
        return response.json()
    except requests.RequestException as e:
        logging.error("GET request failed: %s", e)
        return None

def main(api_url: str, api_key: str, start_date: str):
    logging.info("Application started")
    logging.info("API Key: %s", api_key)

    headers = {
        "api-key": api_key,
        "Accept": "application/json"
    }

    response = do_get_request(f"{api_url}/workouts", headers=headers)

    for workout in response["workouts"]:
        workout_date = datetime.fromisoformat(workout['start_time'])
        logging.info("%s", workout['title']) 
        logging.info("Data: %s", workout_date.strftime("%d-%m-%Y")) 
        exercises = workout['exercises']
        for exercise in exercises:
            logging.info(" - %s", exercise['title'])
            sets = exercise['sets']

            if exercise['title'] == "Treadmill":
                logging.info("    * Distancia: %s metros, Tempo: %s segundos", sets[0]["distance_meters"], sets[0]["duration_seconds"])
            else:
                for s in sets:
                    logging.info("    * Reps: %s, Peso: %s kg", s['reps'], s['weight_kg'])
        logging.info(120*"-")   

if __name__ == "__main__":
    API_URL = "https://api.hevyapp.com/v1"
    API_KEY = os.getenv("API_KEY")
    if not API_KEY:
        logging.error("Environment variable API_KEY is not set")
        sys.exit(1)

    main(api_url=API_URL, api_key=API_KEY, start_date="2025-08-31")