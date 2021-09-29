import json
import os

def parse_id(console):
    filename = input('\nEnter the filename of your collection (with .json): ')

    if len(filename) > 0:
        cardData = json.load(open('input/' + filename))
        
    # Uncomment the line below if you want to bypass the file input and use hardcoded filename.    
    # cardData = json.load(open('input/lands.json'))
    cardData = cardData['entries']['columna']

    cardIds = []
    for card in cardData:
        if card['card_digest'] is not None:
            cardIds.append(
                {
                    'id': card['card_digest']['id'], 
                    'count': card['count']
                }
            )

    cardIdsDict = {
        "identifiers": []
    }

    cardIdsDict['identifiers'] = cardIds

    jsonFilename = "card_ids.json"
    path = 'json/'

    try:
        os.makedirs(path)
    except FileExistsError:
        pass

    with open(path + jsonFilename, 'w', encoding='utf-8') as f:
        json.dump(cardIdsDict, f, ensure_ascii=False, indent=4)

    console.print("GENERATED FILE: ", jsonFilename, style="green")