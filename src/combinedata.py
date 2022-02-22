import json
import re

def combine_data(console):
    """ Filters and combines the data from two JSON file into one final JSON. 

        It opens and reads pre-generated two JSON files with the following keys.
        parseid.py -> cards_ids.json (id, count)
        scrycards.py -> raw_card_data.json (id, name, set, collector_number)

        Generates a filename using the name, set and collector number
        for each card that matches using the id. 

        Parameters:
        Arg1 (rich.console.Console): From the rich package used only to style to console output.
        
        Return: None. Generates a new JSON file. 
            -> combine_card_data.json (id, filename, filename_back, count, total)
    """

    cardIds = json.load(
        open('json/card_ids.json')
    )

    rawCardData = json.load(
        open('json/raw_card_data.json', encoding='utf-8')
    )

    cardList = rawCardData['data']
    combinedCardData = []
    cardCount = 0 # Total images in the collection

    for cardData in cardList:
        cardCount += 1
        cardSet = cardData['set']
        cardId = cardData['id']
        cardCollectorNum = re.sub('\D', '', cardData['collector_number'])
        
        # Some cards are double faced, so two separate filenames have to be generated. 
        # Checks if the current card is double faced. 
        if ('card_faces' in cardData) and ('image_uris' in cardData['card_faces'][0]):
            cardName = cardData['card_faces'][0]['name']
            cardBackName = cardData['card_faces'][1]['name']
            
            """ Generates the image filename in a specific format.
                The format is used later to generate the PDF, so beware when changing the code!
                
                It combines the `set`, `collector_number` and card `name`. 
                The name is lowercased and the white spaces replaced with dashes. 

                Format: [set_code]-[collector_number]-[card-name-separated-with-dashes].png
                Example: The First Sliver (Modern Horizons #200) -> 
                        mh1-200-the-first-sliver.png (single-faced card)
                        mid-17-enduring-angel-front.png (double-faced card)
                        mid-17-angelic-enforcer-back.png
                
                Generates `combined_card_data.json` which is used by `createpdf.py`.
                The format is used again in `downloadimgs.py` to generate `combined_card_data.json` which is used by `createpdf.py`.
            """
            cardFilename = cardSet + '-' + cardCollectorNum + '-' + cardName.replace(" ", "-").lower() + '-front.png'
            cardBackFilename = cardSet + '-' + cardCollectorNum + '-' + cardBackName.replace(" ", "-").lower() + '-back.png'
            
            for inputCard in cardIds['identifiers']:
                if inputCard['id'] == cardId:
                    
                    # How many copies of a unique card are needed.
                    # count - 1, because of the addition cardCount increase,
                    # at the top of the loop.
                    count = inputCard['count']
                    if count > 1:
                        cardCount += count - 1

                    # Adds data to the {} for a double-faced card.
                    combinedCardData.append(
                        {
                            # "id": cardId,
                            "filename": cardFilename,
                            "filename_back": cardBackFilename,
                            "count": count,
                            "total": cardCount
                        }
                    )
        else:
            cardName = cardData['name'].replace("//", "").replace("  ", " ")
            cardFilename = cardSet + '-' + cardCollectorNum + '-' + cardName.replace(" ", "-").lower() + '.png'
            
            for inputCard in cardIds['identifiers']:
                if inputCard['id'] == cardId:

                    count = inputCard['count']
                    if count > 1:
                        cardCount += count - 1

                    # Adds data to the {} for a single-faced card.
                    combinedCardData.append(
                        {
                            # "id": cardId,
                            "filename": cardFilename,
                            "count": count,
                            "total": cardCount
                        }
                    )

    jsonFilename = 'combined_card_data.json'
    path = 'json/'

    # Exports a new JSON file -> json/combined_card_data.json
    with open(path + jsonFilename, 'w', encoding='utf-8') as f:
        json.dump(combinedCardData, f, ensure_ascii=False, indent=4)

    console.print("GENERATED FILE: ", jsonFilename, style="green")