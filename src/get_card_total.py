import json

def get_card_total():
    cardTotal = json.load(
        open('json/combined_card_data.json')
    )

    return list(cardTotal)[-1]['total']

def get_unique_total():
    cardUnique = json.load(
        open('json/combined_card_data.json')
    )

    return len(cardUnique)
