import requests
def get_twitch():
    url = 'https://api.twitch.tv/helix/games/top'
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.get(url, headers=headers)
    return r.json()