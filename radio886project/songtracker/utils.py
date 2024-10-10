import requests

def get_current_song():
    url = "https://radio886.at/api/current-song"  # Ersetzen Sie dies durch die tatsächliche API-URL
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            'title': data.get('title'),
            'artist': data.get('artist')
        }
    return None