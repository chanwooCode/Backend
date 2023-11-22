import requests
import pyrebase
import json
import pytz
from datetime import datetime
from config import api_key
from teamName import team_name_mapping, convert_team_names

# Set the base URL for the Football Data API v4
base_url = "https://api.football-data.org/v4"
# Set the headers with your API key
headers = {
    "X-Auth-Token": api_key,
}

# Function to get standings for a specific competition
def get_standings():
    url = f"{base_url}/competitions/PL/standings"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting standings. Status code: {response.status_code}")
        return None

# Function to get matches for a specific competition
def get_matches():
    url = f"{base_url}/competitions/PL/matches"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting standings. Status code: {response.status_code}")
        return None

def get_current_kst_date():
    kst = pytz.timezone('Asia/Seoul')
    now_utc = datetime.utcnow().replace(tzinfo=pytz.UTC)
    now_kst = now_utc.astimezone(kst)
    return now_kst.strftime('%m-%d %H:%M')
    
with open("auth.json") as f:
    config = json.load(f)
firebase = pyrebase.initialize_app(config)
db = firebase.database()

standings_data = get_standings()
if standings_data:
    # Extract the standings table from the response
    standings_table = standings_data['standings'][0]['table']
    # Create a list to hold the transformed data
    firebase_data = []
    # Transform the data to match the TeamTable structure
    for team_info in standings_table:
        team_data = {
            "rank": team_info["position"],
            "teamName": convert_team_names(team_info["team"]["name"]),
            "matchesPlayed": team_info["playedGames"],
            "wins": team_info["won"],
            "draws": team_info["draw"],
            "losses": team_info["lost"],
            "points": team_info["points"]
        }
        firebase_data.append(team_data)
    # Push the transformed data to Firebase
    db.child("standings").set(firebase_data)
    print("Data saved to Firebase successfully")


def get_current_utc_date():
    now = datetime.utcnow()
    return now.strftime('%Y-%m-%dT%H:%M:%SZ')
    
def convert_utc_to_kst(utc_time_str):
    utc_time = datetime.strptime(utc_time_str, '%Y-%m-%dT%H:%M:%SZ')
    kst = pytz.timezone('Asia/Seoul')
    kst_time = utc_time.replace(tzinfo=pytz.utc).astimezone(kst)
    return kst_time.strftime('%m-%d %H:%M')

# Fetch matches data
matches_data = get_matches()
if matches_data:
    # Extract the matches data from the response
    matches = matches_data['matches']
    # Filter out finished matches
    ongoing_matches = [match for match in matches if match["status"] != "FINISHED"]
    # Sort ongoing matches by proximity to the current time
    matches_sorted = sorted(ongoing_matches, key=lambda x: abs((datetime.strptime(x["utcDate"], '%Y-%m-%dT%H:%M:%SZ') - datetime.strptime(get_current_utc_date(), '%Y-%m-%dT%H:%M:%SZ')).total_seconds()))
    # Create a list to hold the transformed data
    firebase_matches_data = []
    # Limit to the top 10 matches
    for match_info in matches_sorted[:10]:
        home_team_name = convert_team_names(match_info["homeTeam"]["name"])
        away_team_name = convert_team_names(match_info["awayTeam"]["name"])

        match_data = {
            "time": convert_utc_to_kst(match_info["utcDate"]),  # Convert UTC to KST
            "homeTeam": home_team_name,
            "awayTeam": away_team_name,
            "status": match_info["status"],
            # Add more fields as needed
        }
        firebase_matches_data.append(match_data)
    # Push the transformed matches data to Firebase
    db.child("matches").set(firebase_matches_data)
    print("Top 10 matches data saved to Firebase successfully")
