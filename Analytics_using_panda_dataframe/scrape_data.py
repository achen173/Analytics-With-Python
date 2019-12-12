import sys
from urllib.parse import urlparse
import urllib.parse
import csv
import scraper

# Starter code for downloading song lyrics.  To search for a song that contains the phrase
# "road to nowhere", you can call it like this:
# > python scrape_data.py road to nowhere


# First, grab the results page from the search
URL_BASE = 'https://www.zyxware.com/articles/5914/list-of-fortune-500-companies-and-their-websites-2018'
#URL_END = '/history'
#URL_MIDDLE = " ".join(sys.argv[1:2])
#URL_Sec = " ".join(sys.argv[2:])
#print(URL_MIDDLE, URL_Sec)
#URL_MIDDLE = "%5EGSPC"
#url = URL_BASE+URL_MIDDLE+URL_END
stock_scrape = scraper.UrlScraper(URL_BASE)
Rank = stock_scrape.pull_from_to('<th>','</th>')
Name = stock_scrape.pull_from_to('<th>','</th>')
Web = stock_scrape.pull_from_to('<th>','</th>')
wtr = csv.writer(open ('awesome_data.csv', 'w'), delimiter=',', lineterminator='\n')
wtr.writerow([Rank, Name, Web])
# Parse out the artist, song, and url from the top search result.  The code below captures the name
# of the song; you'll need to modify it to grab the artist and url for the lyrics page as well.


for x in range(200):
    Rank = stock_scrape.pull_from_to('<td>', '</td>')
    Name = stock_scrape.pull_from_to('<td>', '</td>')
    Web = stock_scrape.pull_from_to('">', '</a>')
    wtr.writerow([Rank, Name, Web])