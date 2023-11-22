team_name_mapping = {
    "Brighton & Hove Albion FC": "Brighton",
    "AFC Bournemouth": "Bournemouth",
    "Nottingham Forest FC": "Nottingham",
    "Sheffield United FC": "Sheffield",
    "Arsenal FC": "Arsenal",
    "Brentford FC": "Brentford",
    "Aston Villa FC": "Aston Villa",
    "Tottenham Hotspur FC": "Tottenham",
    "Manchester United FC": "Man United",
    "Everton FC": "Everton",
    "Wolverhampton Wanderers FC": "Wolverhampton",
    "Fulham FC": "Fulham",
    "West Ham United FC": "West Ham",
    "Burnley FC": "Burnley",
    "Manchester City FC": "Man City",
    "Liverpool FC": "Liverpool",
    "Crystal Palace FC": "Crystal Palace",
    "Luton Town FC": "Luton Town",
    "Newcastle United FC": "Newcastle",
    "Chelsea FC": "Chelsea"
}

def convert_team_names(team_name):
    # Use the team_name_mapping dictionary to get the abbreviated name
    return team_name_mapping.get(team_name, team_name)