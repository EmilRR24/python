import requests
def get_twitch():
    url = 'https://api.twitch.tv/helix/games/top'
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'Authorization' : 'Bearer 3qbgrg28kobkxs1f184eq8cnmm9fgy', 'Client-Id' : '8b6o67lgkip4190y7u7poqqwno1eme'}
    r = requests.get(url, headers=headers)
    # print(r.json()['data'])
    return r.json()