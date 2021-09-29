import json

def combine_data(console):
    cardIds = json.load(
        open('json/card_ids.json')
    )

    rawCardData = json.load(
        open('json/raw_card_data.json')
    )

    cardList = rawCardData['data']
    combinedCardData = []
    cardCount = 0

    for cardData in cardList:
        cardCount += 1
        cardSet = cardData['set']
        cardId = cardData['id']
        cardCollectorNum = cardData['collector_number']

        if 'card_faces' in cardData:
            cardName = cardData['card_faces'][0]['name']
            cardBackName = cardData['card_faces'][1]['name']
            
            cardFilename = cardSet + '-' + cardCollectorNum + '-' + cardName.replace(" ", "-").lower() + '-front.png'
            cardBackFilename = cardSet + '-' + cardCollectorNum + '-' + cardBackName.replace(" ", "-").lower() + '-back.png'
            
            for inputCard in cardIds['identifiers']:
                if inputCard['id'] == cardId:

                    count = inputCard['count']
                    if count > 1:
                        cardCount += count - 1

                    combinedCardData.append(
                        {
                            "id": cardId,
                            "filename": cardFilename,
                            "filename_back": cardBackFilename,
                            "count": count,
                            "total": cardCount
                        }
                    )
        else:
            cardName = cardData['name']
            cardFilename = cardSet + '-' + cardCollectorNum + '-' + cardName.replace(" ", "-").lower() + '.png'
            
            for inputCard in cardIds['identifiers']:
                if inputCard['id'] == cardId:

                    count = inputCard['count']
                    if count > 1:
                        cardCount += count - 1

                    combinedCardData.append(
                        {
                            "id": cardId,
                            "filename": cardFilename,
                            "count": inputCard['count'],
                            "total": cardCount
                        }
                    )

    jsonFilename = 'combined_card_data.json'
    path = 'json/'

    with open(path + jsonFilename, 'w', encoding='utf-8') as f:
        json.dump(combinedCardData, f, ensure_ascii=False, indent=4)

    console.print("GENERATED FILE: ", jsonFilename, style="green")