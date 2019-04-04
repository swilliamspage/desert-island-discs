# desert-island-discs
A web scraper that downloads desert island discs data.

# code:
**get_links.py**: Saves a csv of urls for each desert island disc episode

**scraper_a.py**: For each castaway with a first name beginning with the letter a this saves a csv file, with each row containing:
 - castaway name
 - date of episode
 - book
 - luxury
 - eight song choices with name, artist, album and musicbrainz id
 
 # data:
 csv files for all castaways, up to October 2018

# to do:
Combine code in to one file where you don't have to save links separately first and then manually change the letter in scraper_a.py