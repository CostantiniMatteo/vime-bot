import json
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))

import requests

TOKEN = os.environ['TELEGRAM_TOKEN']
TWITCH_CLIENT_ID = os.environ['TWITCH_CLIENT_ID']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)
TWITCH_URL = "https://api.twitch.tv/helix/videos?user_id=52650914&first=50"
headers = {'Client-ID': TWITCH_CLIENT_ID}


def get_game_url(team1, team2, game):
    r = requests.get(TWITCH_URL, headers=headers)
    data = r.json()['data']
    for item in data:
        title = item['title']
        if title.find(team1) != -1 and title.find(team2) != -1 \
            and title.find(f"GAME {game}") != -1:
            return item['url']
    return None


def vime_bot(event, context):
    try:
        data = json.loads(event["body"])
        message = str(data["message"]["text"])
        chat_id = data["message"]["chat"]["id"]

        try:
            team1, team2, game = message.upper().split()
            response = get_game_url(team1, team2, game)
            if not response:
                response = "¯\_(ツ)_/¯"
        except Exception as e:
            response = "¯\_(ツ)_/¯"

        data = {"text": response.encode("utf8"), "chat_id": chat_id}
        url = BASE_URL + "/sendMessage"
        requests.post(url, data)

    except Exception as e:
        print(e)

    return { "statusCode": 200 }
