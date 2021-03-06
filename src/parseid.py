import json
import os

def parse_id(console):
    """ Filters through a given JSON file and exports the ID and Count into another JSON file. 

        It opens and reads the user inputted card collection in JSON format from Scryfall.
        [filename].json -> cards_ids.json (id, count)

        The input filename is taken from user input or it can be hardcoded. 
        The file should be placed into the /input directory, otherwise the script will not run. 

        Parameters:
        Arg1 (rich.console.Console): From the rich package used only to style to console output.
        
        Return: None. Generates a new JSON file. 
            -> cards_ids.json (id, count)
    """

    INPUT_PATH = "input/"
    DEFAULT_FILENAME = "Lands.json"
    
    filename = input('\nEnter the filename of your collection (with .json): ')

    # Checks if the filename has not been entered by the user
    if len(filename) == 0:
        filename = DEFAULT_FILENAME

    deckData = json.load(open(INPUT_PATH + filename))

    cardIds = []
    # This loop goes through each category / section. (commanders, lands, nonlands, sideboard, etc.)
    for section in deckData['entries']:
        cardData = deckData['entries'][section]
        
        for card in cardData:
            # If the key 'card_digest' does not exist or its empty, the item is not a valid card. 
            if card['card_digest'] is not None:
                cardIds.append(
                    {
                        'id': card['card_digest']['id'], 
                        'count': card['count']
                    }
                )

    """ The result JSON has to be formated in this way to be accepted later by the Scryfall API.

        `cards_ids.json` is used by 'scrycards.py' and 'combinedata.py'
    """
    cardIdsDict = {
        "identifiers": []
    }

    cardIdsDict['identifiers'] = cardIds

    jsonFilename = "card_ids.json"
    JSON_PATH = 'json/'

    # Creates JSON_PATH directory, if it does not exist. 
    try:
        os.makedirs(JSON_PATH)
    except FileExistsError:
        pass

    # Exports a new JSON file -> json/cards_ids.json
    with open(JSON_PATH + jsonFilename, 'w', encoding='utf-8') as f:
        json.dump(cardIdsDict, f, ensure_ascii=False, indent=4)

    console.print("GENERATED FILE: ", jsonFilename, style="green")

    return filename