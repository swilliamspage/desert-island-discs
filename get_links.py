from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os,sys
from time import sleep
from random import randint
import requests
from urllib.parse import urljoin

#TO DO:
#1. Make bio failsafe
#2. When code fails, print out which artist it got up to
#3. Ideally then allow code to start up again from next castaway rather than starting all over again


os.chdir("/Users/sianwilliams/Desktop/fiveh/DesertIslandDiscs/scraper_python")
sys.path.append(os.getcwd())
from string import ascii_lowercase
for c in ascii_lowercase:
    alphabet_a = "https://www.bbc.co.uk/programmes/b006qnmr/episodes/a-z/"+c
    print(alphabet_a)
    start_url = 'https://www.bbc.co.uk/'
    
    #driver = webdriver.Chrome()
    driver = webdriver.Chrome(executable_path='/Users/sianwilliams/Desktop/fiveh/DesertIslandDiscs/scraper_python/chromedriver.exe')
    
    driver.implicitly_wait(30)
    driver.get(alphabet_a)
    sleep(randint(1,3))
    
    
    
    #scroll to the bottom of the page to get all castaways with firstname starting with chosen letter
    SCROLL_PAUSE_TIME = 11
    
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # Wait to load page
        sleep(SCROLL_PAUSE_TIME)
    
     # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        print(new_height)
        if new_height == last_height:
            break
        last_height = new_height
    
    
    #get html
    alphabetHTML = driver.execute_script("return document.body.innerHTML")
    sleep(randint(1,3))
    alphabetsoup =  BeautifulSoup(alphabetHTML,'html.parser')
    
    #print html to text file to allow examination of structure of list of castaways
    text_file_a = open("alphabet_html.txt","w")
    text_file_a.write(alphabetsoup.prettify())
    text_file_a.close()
    
    a_tags = alphabetsoup.find_all('a', class_='box-link__target link--block ',href=re.compile(r"^/programmes/"))
    links = [urljoin(start_url, a['href'])for a in a_tags]
    print(links)
    
    sav_name = "linksv3_"+c+".txt"
    links_file = open(sav_name,"w")
    for l in links:
        links_file.write(l+ '\n')
    links_file.close()
