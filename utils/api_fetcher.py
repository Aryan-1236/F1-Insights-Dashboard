import requests
import pandas as pd
import os

def fetch_driver_standings(season=2023):
    url = f"http://ergast.com/api/f1/{season}/driverStandings.json?limit=1000"
    response = requests.get(url)
    data = response.json()

    standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
    rows = []
    for d in standings:
        driver = d['Driver']
        rows.append({
            'position': int(d['position']),
            'points': float(d['points']),
            'wins': int(d['wins']),
            'driver': f"{driver['givenName']} {driver['familyName']}",
            'nationality': driver['nationality'],
            'constructor': d['Constructors'][0]['name']
        })

    df = pd.DataFrame(rows)
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/driver_standings_2023.csv", index=False)
    print("✅ Driver standings saved successfully.")

if __name__ == "__main__":
    fetch_driver_standings()
