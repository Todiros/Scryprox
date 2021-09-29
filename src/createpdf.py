import json
from fpdf import FPDF
from datetime import datetime
import os

def create_pdf(console, print, track, totalCount):
    console.print("\nPreparing to import images...\n", style="bold yellow")

    countedCards = json.load(
        open('json/combined_card_data.json')
    )

    class PDF(FPDF):
        # Page footer
        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-15)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            # Page number
            self.cell(0, 20, 'Page ' + str(self.page_no()), 0, 0, 'R')

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

    for card in track(countedCards, description="[magenta]Creating PDF... "):
        i = card['count']

        while i > 0:
            pdf.image('png/'+card['filename'], nextX, nextY, cardWidth, cardHeight)
            totalCards += 1
            print(card['filename'] + " has been added to the PDF. [", totalCards, "/", totalCount, "]")

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
    filename = PDF_PATH + 'proxies-' + dateStr + '.pdf'

    console.print("\nGenerating file...", style="yellow")

    try:
        os.makedirs(PDF_PATH)
    except FileExistsError:
        pass    
    
    pdf.output(filename, 'F')
    console.print("\nGENERATED FILE: ", filename, "\n", style="bold green")