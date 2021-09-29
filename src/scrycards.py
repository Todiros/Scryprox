import json
import requests

def scry_cards(console):
    jsonFile = open('json/card_ids.json')
    cardIds = json.load(jsonFile)

    res = requests.post("https://api.scryfall.com/cards/collection", json=cardIds)
    cardData = res.json()

    jsonFilename = 'raw_card_data.json'
    path = 'json/'

    with open(path + jsonFilename, 'w', encoding='utf-8') as f:
        json.dump(cardData, f, ensure_ascii=False, indent=4)

    console.print("GENERATED FILE: ", jsonFilename, style="green")