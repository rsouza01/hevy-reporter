#!/usr/bin/env python3

import logging
import sys
import requests
import os
from datetime import datetime
import argparse

# Drop the loglevel
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(message)s')

def do_get_request(url: str, headers: dict):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logging.info("GET request successful: %s", response.status_code)
        return response.json()
    except requests.RequestException as e:
        logging.error("GET request failed: %s", e)
        return None

def print_workout_details(workouts: dict, verbose: bool = False):
    for index, workout in enumerate(workouts, start=1):
        workout_date = datetime.fromisoformat(workout['start_time'])
        logging.info("%d) %s", index, workout['title']) 
        logging.info("Data: %s", workout_date.strftime("%d-%m-%Y"))
        if verbose:
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


def main(api_url: str, api_key: str, start_date):
    logging.info("Application started")
    logging.info("API Key: %s", api_key)
    logging.info("start_date: %s", start_date)

    headers = {
        "api-key": api_key,
        "Accept": "application/json"
    }

    workouts = []
    fetch_next = True
    page_number = 1
    while fetch_next == True:
        logging.info(f"Fetching page {page_number}...")
        response = do_get_request(f"{api_url}/workouts?page={page_number}&pageSize=10", headers=headers)
        workouts.extend(response["workouts"])
        page_number = page_number + 1
        if page_number > 4 or len(response["workouts"]) == 0:
            fetch_next = False


    print_workout_details(workouts, verbose=True)

def parse_args():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Data de início dos treinos.")
    parser.add_argument("start_date", type=str, help="format YYYY-MM-DD")

    # Parse arguments
    args = parser.parse_args()

    start_date = None

    # Validate and convert to date
    try:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d").date()
        print(f"Start date is: {start_date}")
    except ValueError:
        print("Error: start_date must be in YYYY-MM-DD format.")

    return start_date

if __name__ == "__main__":
    API_URL = os.getenv("HEVY_API_URL")
    if not API_URL:
        logging.error("Environment variable HEVY_API_URL is not set")
        sys.exit(1)
    API_KEY = os.getenv("HEVY_API_KEY")
    if not API_KEY:
        logging.error("Environment variable HEVY_API_KEY is not set")
        sys.exit(1)

    start_date = parse_args()

    main(api_url=API_URL, api_key=API_KEY, start_date=start_date)