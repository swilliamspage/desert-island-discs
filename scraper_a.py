from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from bs4 import BeautifulSoup
import re
import pandas as pd
import os,sys
from time import sleep
from random import randint
import requests
from urllib.parse import urljoin



#TO DO:
#if inner html doesn't load then reattempt max number of three times


os.chdir("/Users/sianwilliams/Desktop/fiveh/DesertIslandDiscs/scraper_python")
sys.path.append(os.getcwd())
letter = 'a'
alphabet_a = "https://www.bbc.co.uk/programmes/b006qnmr/episodes/a-z/"+letter

start_url = 'https://www.bbc.co.uk/'

savfilname = letter+"_desert_island_database.csv"
linkfile = "linksv3_"+letter+".txt"

#driver = webdriver.Chrome()
driver = webdriver.Chrome(executable_path='/Users/sianwilliams/Desktop/fiveh/DesertIslandDiscs/scraper_python/chromedriver.exe')
browser = driver

#open file with list of desert island disc links - saved using get_links.py
link_file = open(linkfile,"r")
links = link_file.readlines()
link_file.close()

print('This many links')
print(len(links))
#create csv with correct headings
header_df = pd.DataFrame(columns=['Castaway', 'Date','Book',
        'Luxury', 'Song1','Song2','Song3','Song4','Song5','Song6','Song7',
        'Song8','Artist1','Artist2','Artist3','Artist4','Artist5',
        'Artist6','Artist7','Artist8',
        'Album1','Album2','Album3','Album4','Album5','Album6','Album7','Album8',
        'Short desc','Bio','ID1','ID2','ID3','ID4','ID5','ID6','ID7','ID8',
        'Favourite','Error','Url'])

header_df.to_csv(savfilname)

#loop over urls here 
for link in links[0:len(links)]:
#for link in links[114:115]:

#allow eight attempts to load the inner html - tested by whether we get the song details (probably a better way of doing this) - break the loop if the length of the song names doesn't equal zero and save to file


    counter = 0
    for counter in range(30):
        counter = counter+1
        print('attempt number')
        print(counter)

        browser.implicitly_wait(30)
        page = browser.get(link)
        sleep(10)
    
        SCROLL_PAUSE_TIME = 10
    
    # Scroll down the window - need to do this to load the record info
        last_height = browser.execute_script("return document.body.scrollHeight")
        scroll_command1 = "window.scrollTo(0, "
        scroll_command2 = ");"
    
        heights = [200,500,800,1000,1200,1350,1500,1750,2000,2500]
        for h in heights:
            height_str = str(h)
            scroll_command_all1 = scroll_command1+height_str+scroll_command2
            browser.execute_script(scroll_command_all1)
            sleep(randint(3,5))
        
        #driver.get(url) #navigate to page behind login
        innerHTML = driver.execute_script("return document.body.innerHTML") 
        #returns the inner HTML as a string
    
        sleep(randint(1,3))
        soup = BeautifulSoup(innerHTML, 'html.parser')
        #print(soup.prettify())
    
        #print html to text file to allow examination of structure
        text_file = open("innerhtmltest_mostrec.txt", "w")
        text_file.write(soup.prettify())
        text_file.close()
    
        #find castaway name
        castaway_name = soup.select('h1.no-margin')
        castaway=[]
        for castaway_n in castaway_name:
            castaway.append(castaway_n.get_text())
        print(castaway)
    
        #find castaway bio
        castaway_bio_s = soup.find_all('div', class_ = 'ml__content prose text--prose')
        castaway_bio=[]
        for castaway_bio_n in castaway_bio_s:
            castaway_bio.append(castaway_bio_n.get_text())
        print(castaway_bio)
        if len(castaway_bio) == 0:
            castaway_bio = [' ']
    
    
        #find book and luxury
        bl_s = soup.select('span.title')
        bl=[]
        for bl_n in bl_s:
            bl.append(bl_n.get_text())
        print(bl)
        print(len(bl))
        if len(bl)>1:
            book = bl[0]
            luxury = bl[1]
        else:
            book=''
            luxury=''  
        print(book)
        print(luxury)
    
        #find release date 
        release_s = soup.find_all('span', class_='broadcast-event__date text-base timezone--date')
        print('printing release ', release_s)
        release=[]
        for release_n in release_s:
            release.append(release_n.get_text())
        print(release)
        if len(release)>0:
            date = release[0]        
        else:
            date = ''
        print(date)



        #find artist id for music brainz
        mb_id = []
        artist_fromdata = []
        song_fromdata = []
        idchecks = []
        #alldivs = soup.find_all("div", {"class" : "spt-snippet spt-theme-default"})
        alldivs = soup.find_all("div")
        #print(alldivs)
        for d in alldivs:
            id_c = d.get('data-artist-id')
            if isinstance(id_c, str):
                mb_id.append(id_c)
            #if(d.attrs['data-artist-id']):
            #    mb_id.append(d.attrs['data-artist-id'])
            artist_c = d.get('data-artist')
            if isinstance(artist_c, str):
                artist_fromdata.append(artist_c)
            song_c = d.get('data-title')
            if isinstance(song_c, str):
                song_fromdata.append(song_c)
        print(mb_id)
        print(artist_fromdata)
        print(song_fromdata)
        if len(mb_id) != 8:
            mb_id = [' ',' ',' ',' ',' ',' ',' ',' ']
               
        
        #    if len(idcheck) > 0:
        #        print('found an id!')
        #        print(idcheck)
        #        mb_id.append(idcheck)
    
    
       
    
        #check here whether inner html has loaded - sometimes it doesn't work. If not, reload webpage
        
        
        #trying to deal with issue when number of artists doesnt match number of songnames - ie when there are old tracks or tracks with collabroations (e.g. alex crawford)
        
        albums = []
        fav = []
        alltracks = soup.find_all("div", {"class" : "segment__track"})  
        print('Printing all track info')
        for r in alltracks:
            album_select = r.find_all('em')
            if len(album_select) == 1:
                for al in album_select:
                    albums.append(al.get_text())
            else:
                albums.append('None')
        #find count of favourite song - might be nice
                
        #find occupation
        info = []
        occu_info = soup.find_all("div", {"class" : "text--prose longest-synopsis"})
        print(occu_info)
        for x in occu_info:
             info.append(x.get_text())
        if len(info) == 0:
        #try alternative method - some have slightly different structure
            occu_info_try2 = soup.find_all("div", {"class" : "synopsis-toggle__short"})
            print('trying alternative method of getting occupation info', occu_info_try2)
            for y in occu_info_try2:
                info.append(y.get_text())
        if len(info) == 0:
            info = ['']
        print(info)
         
        print(info)            
        print('length of song info')
        print(len(song_fromdata)) 
        if len(song_fromdata) != 0:
            print('Seems this attempt has worked so saving to file now')
            break    
    #if all ok then save into dataframe for printing in to csv
    #hitting an error here so trying to figure out whats going on
    if len(song_fromdata) == 8 and len(artist_fromdata) == 8:
        print('This castaway has all relevant info!')
    #    print(len(header_df))
        print(link)
        print(castaway)
        errcode = '0'
        #compile all the data for one castaway into a dataframe with just one row
        print(castaway[0])
        print(date)
        print(book)
        print(luxury)
        print(song_fromdata)
        print(artist_fromdata)
        print(albums) 
        print(info)
        print(castaway_bio)
        print(mb_id)
        print(errcode)
        print(link)
        print(type(castaway_bio[0]))
        df = pd.DataFrame({'Castaway': castaway[0],
            'Date': date,
            'Book': book,
            'Luxury': luxury,
            'Song1': song_fromdata[0],
            'Song2': song_fromdata[1],
            'Song3': song_fromdata[2],
            'Song4': song_fromdata[3],
            'Song5': song_fromdata[4],
            'Song6': song_fromdata[5],
            'Song7': song_fromdata[6],
            'Song8': song_fromdata[7],
            'Artist1': artist_fromdata[0],
            'Artist2': artist_fromdata[1],
            'Artist3': artist_fromdata[2],
            'Artist4': artist_fromdata[3],
            'Artist5': artist_fromdata[4],
            'Artist6': artist_fromdata[5],
            'Artist7': artist_fromdata[6],
            'Artist8': artist_fromdata[7],
            'Album1': albums[0],
            'Album2': albums[1],
            'Album3': albums[2],
            'Album4': albums[3],
            'Album5': albums[4],
            'Album6': albums[5],
            'Album7': albums[6],
            'Album8': albums[7],
            'Short desc': info[0],
           'Bio': castaway_bio[0],
            'ID1': mb_id[0],
            'ID2': mb_id[1],
            'ID3': mb_id[2],
            'ID4': mb_id[3],
            'ID5': mb_id[4],
            'ID6': mb_id[5],
            'ID7': mb_id[6],
            'ID8': mb_id[7],
            'Favourite': ' ',
            'Error': [errcode[0]],
            'url': link})
#        df = pd.DataFrame(compiled_data, columns = ['Castaway', 'Date','Book',
#            'Luxury', 'Song1','Song2','Song3','Song4','Song5','Song6','Song7',
#            'Song8','Artist1','Artist2','Artist3','Artist4','Artist5',
#            'Artist6','Artist7','Artist8','Bio','Error'])
        print(df)
        
        df.to_csv(savfilname,mode='a',header=False)
    else:
        print('Error with this castaway:')
        print(castaway[0])
        errcode = '1'
        songs_together = ''.join(song_fromdata)
        print(songs_together)
        artists_together = ''.join(artist_fromdata)        
        print(artists_together)
        f = open("failedcastaways.txt", "a")
        f.write(castaway[0])
        f.close()
        df = pd.DataFrame({'Castaway': castaway[0],
            'Date': date,
            'Book': book,
            'Luxury': luxury,
            'Song1': songs_together,
            'Song2': ' ',
            'Song3': ' ',
            'Song4': ' ',
            'Song5': ' ',
            'Song6': ' ',
            'Song7': ' ',
            'Song8': ' ',
            'Artist1': artists_together,
            'Artist2': ' ',
            'Artist3': ' ',
            'Artist4': ' ',
            'Artist5': ' ',
            'Artist6': ' ',
            'Artist7': ' ',
            'Artist8': ' ',
            'Album1': ' ',
            'Album2': ' ',
            'Album3': ' ',
            'Album4': ' ',
            'Album5': ' ',
            'Album6': ' ',
            'Album7': ' ',
            'Album8': ' ',
            'Short desc': info,
           'Bio': castaway_bio[0],
            'ID1': mb_id[0],
            'ID2': mb_id[1],
            'ID3': mb_id[2],
            'ID4': mb_id[3],
            'ID5': mb_id[4],
            'ID6': mb_id[5],
            'ID7': mb_id[6],
            'ID8': mb_id[7],
            'Favourite':' ',
            'Error': [errcode],
            'url': link})
#        df = pd.DataFrame(compiled_data, columns = ['Castaway', 'Date','Book',
#            'Luxury', 'Song1','Song2','Song3','Song4','Song5','Song6','Song7',
#            'Song8','Artist1','Artist2','Artist3','Artist4','Artist5',
#            'Artist6','Artist7','Artist8','Bio','Error'])
        print(df)        
        df.to_csv(savfilname,mode='a',header=False)


         
