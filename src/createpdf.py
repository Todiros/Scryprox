import json
from fpdf import FPDF
from datetime import datetime
import os

def create_pdf(console, print, track, totalCount):
    """ Imports the card images into a PDF file and saves the file. 

        It open and reads pre-generated JSON file with the image names and count. 
        combinedata.py -> combine_card_data.json (filename, filename_back, count, total)

        Parameters:
        Arg1, Arg2, Arg3: From the rich package used only to style to console output.
        Arg4 (int): Total count of card images to import. It's also used for styling.   

        Return: None. Generates a new PDF file with the current timestamp.
            -> pdf/proxies-29-09-21-05-23.pdf
    """
    console.print("\nPreparing to import images...\n", style="bold yellow")

    countedCards = json.load(
        open('json/combined_card_data.json')
    )

    class PDF(FPDF):
        # Page footer
        def footer(self):
            self.set_y(-15) # Position at 1.5 cm from bottom
            self.set_font('Arial', 'I', 8)
            self.cell(0, 20, 'Page ' + str(self.page_no()), 0, 0, 'R') # Page number

    # Sets the orientation, units and format of the page.
    pdf = PDF('P', 'mm', 'A4')
    pdf.set_font('Helvetica', 'B', 14)

    spacer = 2
    cardWidth = 63
    cardHeight = 88
    startX = 8
    startY = 15

    nextX = startX
    nextY = startY

    counterX = 0
    cardsPerPage = 0
    totalCards = 0

    pdf.add_page()

    # Using track() from the rich package. It creates a progress bar in the console. 
    # This loop goes through each unique card. 
    for card in track(countedCards, description="[magenta]Creating PDF... "):
        
        # This loop goes through each copy of a unique card. 
        i = card['count']
        while i > 0:
            pdf.image('png/'+card['filename'], nextX, nextY, cardWidth, cardHeight)
            totalCards += 1
            print(card['filename'] + " has been added to the PDF. [", totalCards, "/", totalCount, "]")

            # Moves to the next column of the PDF. 
            nextX = nextX + cardWidth + spacer
            counterX += 1
            cardsPerPage += 1

            # Moves to the next row of the PDF. 
            if counterX == 3:
                nextY = nextY + cardHeight + spacer
                nextX = startX
                counterX = 0

            # Adds and moves to a new page of the PDF.
            if cardsPerPage == 9:
                pdf.add_page()
                nextX = startX
                nextY = startY
                cardsPerPage = 0

            # If the key 'filename_back' exist, the card is double-faced,
            # and a second image (of the back) needs to added to the PDF.
            if 'filename_back' in card:
                pdf.image('png/'+card['filename_back'], nextX, nextY, cardWidth, cardHeight)
                totalCards += 1
                print(card['filename_back'] + " has been added to the PDF. [", totalCards, "/", totalCount, "]")

                nextX = nextX + cardWidth + spacer
                counterX += 1
                cardsPerPage += 1

                if counterX == 3:
                    nextY = nextY + cardHeight + spacer
                    nextX = startX
                    counterX = 0

                if cardsPerPage == 9:
                    nextX = startX
                    nextY = startY
                    cardsPerPage = 0
                    pdf.add_page()

            i -= 1

    now = datetime.now()
    dateStr = now.strftime("%d-%m-%y-%H-%M")
    PDF_PATH = 'pdf/'

    # pdf/proxies-29-09-21-05-23.pdf
    filename = PDF_PATH + 'proxies-' + dateStr + '.pdf'

    console.print("\nGenerating file...", style="yellow")

    # Creates PDF_PATH directory, if it does not exist. 
    try:
        os.makedirs(PDF_PATH)
    except FileExistsError:
        pass    
    
    # Exports the compiled PDF
    pdf.output(filename, 'F')
    console.print("\nGENERATED FILE: ", filename, "\n", style="bold green")