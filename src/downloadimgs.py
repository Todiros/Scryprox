import urllib.request
import json
import os
import time

def download_imgs(console, print, track, uniqueCount):
    console.print("\nInitiating download...\n", style="bold yellow")
    
    rawCardData = json.load(
        open('json/raw_card_data.json')
    )

    cardList = rawCardData['data']
    dlCount = 0
    IMG_PATH = 'png/'

    try:
        os.makedirs(IMG_PATH)
    except FileExistsError:
        pass

    for cardData in track(cardList, description="[magenta]Downloading... "):
        cardSet = cardData['set']
        cardCollectorNum = cardData['collector_number']

        cardBackImgUri = ''
        if 'card_faces' in cardData:
            cardImgUri = cardData['card_faces'][0]['image_uris']['png']
            cardBackImgUri = cardData['card_faces'][1]['image_uris']['png']
            cardName = cardData['card_faces'][0]['name']
            cardBackName = cardData['card_faces'][1]['name']
            
            cardFilename = cardSet + '-' + cardCollectorNum + '-' + cardName.replace(" ", "-").lower() + '-front.png'
            cardBackFilename = cardSet + '-' + cardCollectorNum + '-' + cardBackName.replace(" ", "-").lower() + '-back.png'
            
            urllib.request.urlretrieve(cardImgUri, IMG_PATH + cardFilename)
            
            dlCount += 1
            print(cardFilename + " downloaded. [", dlCount, "/", uniqueCount, "]")
            
            time.sleep(0.1)
            
            urllib.request.urlretrieve(cardBackImgUri, IMG_PATH + cardBackFilename)
            
            print(cardBackFilename + " downloaded.")
        else:
            cardImgUri = cardData['image_uris']['png']
            cardName = cardData['name']
            cardFilename = cardSet + '-' + cardCollectorNum + '-' + cardName.replace(" ", "-").lower() + '.png'
            
            urllib.request.urlretrieve(cardImgUri, IMG_PATH + cardFilename)
            
            dlCount += 1
            print(cardFilename + " downloaded. [", dlCount, "/", uniqueCount, "]")
        
        time.sleep(0.1)

    console.print("\nDownload complete!", style="bold green")