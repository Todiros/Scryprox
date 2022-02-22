import urllib.request
import json
import os
import time
import re

def download_imgs(console, print, track, uniqueCount):
    """ Downloads card images from Scryfall API. 

        It open and reads pre-generated JSON file with the image URIs.
        scrycards.py -> raw_card_data.json

        Parameters:
        Arg1, Arg2, Arg3: From the rich package used only to style to console output.
        Arg4 (int): Total count of unique images for download. It's also used for styling.   

        Return: None
    """
    console.print("\nInitiating download...\n", style="bold yellow")
    
    rawCardData = json.load(
        open('json/raw_card_data.json', encoding='utf-8')
    )

    cardList = rawCardData['data']
    dlCount = 0 # Downloaded cards count.
    IMG_PATH = 'png/'

    # Creates IMG_PATH directory, if it does not exist. 
    try:
        os.makedirs(IMG_PATH)
    except FileExistsError:
        pass

    # Using track() from the rich package. It creates a progress bar in the console. 
    for cardData in track(cardList, description="[magenta]Downloading... "):
        cardSet = cardData['set']
        cardCollectorNum = re.sub('\D', '', cardData['collector_number'])

        cardBackImgUri = ''
        # Some cards are double faced, so two separate images have to be downloaded. 
        # Checks if the current card is double faced. 
        if ('card_faces' in cardData) and ('image_uris' in cardData['card_faces'][0]):
            cardImgUri = cardData['card_faces'][0]['image_uris']['png']
            cardBackImgUri = cardData['card_faces'][1]['image_uris']['png']
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
                
                The format is used again in `combinedate.py` to generate `combined_card_data.json` which is used by `createpdf.py`.
            """
            cardFilename = cardSet + '-' + cardCollectorNum + '-' + cardName.replace(" ", "-").lower() + '-front.png'
            cardBackFilename = cardSet + '-' + cardCollectorNum + '-' + cardBackName.replace(" ", "-").lower() + '-back.png'
            
            # Downloading the FRONT face of a double-faced card.
            urllib.request.urlretrieve(cardImgUri, IMG_PATH + cardFilename)
            
            # Even though it downloads two images, the count goes up once, because its considered a single card. 
            dlCount += 1
            print(cardFilename + " downloaded. [", dlCount, "/", uniqueCount, "]")
            
            """ Mandatory, in order to avoid overloading Scryfall's servers! """ 
            time.sleep(0.1)
            
            # Downloading the BACK face of a double-faced card.
            urllib.request.urlretrieve(cardBackImgUri, IMG_PATH + cardBackFilename)
            
            print(cardBackFilename + " downloaded.")
        else:
            cardImgUri = cardData['image_uris']['png']
            cardName = cardData['name'].replace("//", "").replace("  ", " ")
            cardFilename = cardSet + '-' + cardCollectorNum + '-' + cardName.replace(" ", "-").lower() + '.png'
            
            # Downloading the image of a single-faced card.
            urllib.request.urlretrieve(cardImgUri, IMG_PATH + cardFilename)
            
            dlCount += 1
            print(cardFilename + " downloaded. [", dlCount, "/", uniqueCount, "]")
        
        time.sleep(0.1)

    console.print("\nDownload complete!", style="bold green")