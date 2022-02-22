import json
import requests
import time 
from src.splitJson import split_json

def scry_cards(console):
    """ It sends a POST request with JSON file to Scryfall API. Generates new JSON file with the response.   
        
        The input JSON file contains the ids of all of the requested cards.
        With a single request, Scryfall returns all of the data for each card with the respected id. 

        card_ids.json (id, count) -> POST Scryfall API -> raw_card_data.json

        Parameters:
        Arg1 (rich.console.Console): From the rich package used only to style to console output.
        
        Return: None. Generates a new JSON file. 
            -> raw_card_data.json
    """

    jsonFile = open('json/card_ids.json')
    cardIds = json.load(jsonFile)

    # split_json(json_filename) splits the full card list into multiple chunks with 75 objects (cards) each.
    # This is to accommodate Scryfall' 75 card limit per request.
    splits = split_json(cardIds)
    splitRes = []
    
    for part in splits:
        res = requests.post("https://api.scryfall.com/cards/collection", json=part)
        splitRes.append(res.json())
        time.sleep(0.1)

    # Assigns the first chunk (card list) in its entire form, 
    # so then the rest of deck could be appended to the data array property
    cardData = splitRes[0]
    
    # Merging the chunks into the full card list.
    counter = 0
    for jsonRes in splitRes:
        # Skips the first portion as it is already in cardData
        if counter > 0:
            cardData["data"] += jsonRes["data"]
        counter += 1

    jsonFilename = 'raw_card_data.json'
    JSON_PATH = 'json/'

    # Exports a new JSON file -> json/raw_card_data.json
    with open(JSON_PATH + jsonFilename, 'w', encoding='utf-8') as f:
        json.dump(cardData, f, ensure_ascii=False, indent=4)

    console.print("GENERATED FILE: ", jsonFilename, style="green")