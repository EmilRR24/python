import requests
def get_twitch():
    url = 'https://api.twitch.tv/helix/games/top'
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8',}
    r = requests.get(url, headers=headers)
    # print(r.json()['data'])
    return r.json()
