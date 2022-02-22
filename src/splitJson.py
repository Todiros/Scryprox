"""
Takes a deck list (the output of parseid.py) in JSON format. 
Splits it into multiple chunks of 75 objects (cards) or less. 
Due to Scryfall's limit of 75 cards per request.
"""
def split_json(wholeDeckObj):
    # Assign the array with the actual cards (objects)
    wholeDeckArr = wholeDeckObj["identifiers"]

    splits = []
    splits.append({"identifiers": []})

    counter = 0
    splitCounter = 0

    for cardId in wholeDeckArr:
        # For each 76th card, create and start filling a new chunk.
        if(counter == 75):
            splitCounter = splitCounter + 1
            counter = 0
            splits.append({"identifiers": []})    
        
        splits[splitCounter]["identifiers"].append(cardId)
        counter = counter + 1 

    return splits

