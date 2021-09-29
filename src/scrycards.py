import json
import requests

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

    res = requests.post("https://api.scryfall.com/cards/collection", json=cardIds)
    cardData = res.json()

    jsonFilename = 'raw_card_data.json'
    JSON_PATH = 'json/'

    # Exports a new JSON file -> json/raw_card_data.json
    with open(JSON_PATH + jsonFilename, 'w', encoding='utf-8') as f:
        json.dump(cardData, f, ensure_ascii=False, indent=4)

    console.print("GENERATED FILE: ", jsonFilename, style="green")