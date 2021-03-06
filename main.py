from src.parseid import parse_id
from src.scrycards import scry_cards
from src.combinedata import combine_data
from src.downloadimgs import download_imgs
from src.createpdf import create_pdf
from src.get_card_total import get_card_total, get_unique_total
from rich.console import Console
from rich import print
from rich.progress import track

""" Launch the app from here.

It requires a JSON file with a card collection exported from Scryfall. 
The file should be placed into the `input/` directory. Otherwise the script will fail.  
"""

console = Console()

filename = parse_id(console)
scry_cards(console)
combine_data(console)

# Count of unique cards and total cards.
# FIXME: change the variable names to be more accurate.
uniqueCount = get_unique_total()
totalCount = get_card_total()

download_imgs(console, print, track, uniqueCount)
create_pdf(console, print, track, totalCount, filename)