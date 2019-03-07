from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
import re
import os
import urllib
import time
from random import randint


UNIVERSITIES_CACHE_FILE = "universities.txt"

base_url = "https://www.usnews.com/"
university_urls = ['https://www.usnews.com/best-colleges/rankings/national-universities?_page=1',\
                   'https://www.usnews.com/best-colleges/rankings/national-universities?_page=2',\
                   'https://www.usnews.com/best-colleges/rankings/national-universities?_page=3',\
                   'https://www.usnews.com/best-colleges/rankings/national-universities?_page=4',\
                   'https://www.usnews.com/best-colleges/rankings/national-universities?_page=5',\
                   'https://www.usnews.com/best-colleges/rankings/national-universities?_page=6',\
                   'https://www.usnews.com/best-colleges/rankings/national-universities?_page=7',\
                   'https://www.usnews.com/best-colleges/rankings/national-universities?_page=8',\
                   'https://www.usnews.com/best-colleges/rankings/national-universities?_page=9',\
                   'https://www.usnews.com/best-colleges/rankings/national-universities?_page=10']

# placeholder to store the top N universities
universities = []



def getUniversityAddress(driver,university_name):
    query_string = '"'+university_name+'" "address"'
    g_input = driver.find_element_by_name("q")
    g_input.clear()
    g_input.send_keys(query_string)
    g_input.send_keys(Keys.RETURN)

    time.sleep(2)

    # scrape address from results
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #code_soup = soup.find_all('div', attrs={'class': 'kp-hc'})
    #code_soup = soup.find_all('div', attrs={'data-dtype': 'd3ifr'})
    code_soup = soup.find_all('div', attrs={'class': 'Z0LcW'})

    #print("Code Soup: " + str(code_soup[0].get_text()))
    if len(code_soup) > 0:
        address = str(code_soup[0].get_text())
    else:
        address = ""


    return address



def scrapeUrl(universities_url):
    #print("Scraping ", universities_url)
    # Firefox session
    driver = webdriver.Firefox()
    driver.get(universities_url)
    driver.implicitly_wait(10)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    code_soup = soup.find_all('div', attrs={'class': 'shadow-dark block-flush'})

    universities = []
    for i in code_soup:
        #   print(str(i.getText()))
        university_links = i.find_all('h3', attrs={'class':'heading-large block-tighter'})
        for link in university_links:
            universities.append(link.find('a').contents[0])

    # close the browser
    driver.close()

    return universities



if Path(UNIVERSITIES_CACHE_FILE).exists():
    print("cachefile found, reading it")
    # cache file exists, read it rather than scraping the usnews site again
    universities_fh = open(UNIVERSITIES_CACHE_FILE,"r")
    for university in universities_fh:
        universities.append(university)
    universities_fh.close()

# save all universities to text file
if not Path(UNIVERSITIES_CACHE_FILE).is_file():
    # cache file did not exist, scrape the usnews site to grab the universities
    for university_url in university_urls:
        universities = universities + scrapeUrl(university_url)

    # store the universities info to a cache file
    universities_fh = open(UNIVERSITIES_CACHE_FILE,"w")
    for university in universities:
        universities_fh.write(university+"\n")
    universities_fh.close()


# initialize Firefox session
driver = webdriver.Firefox()
driver.get("https://www.google.com")
time.sleep(1)


for university in universities:
    print(university.rstrip(),end=',')
    addr = getUniversityAddress(driver, university)
    city = ''
    state = ''
    if len(addr) > 0:
        # check if street address is given
        if len(re.findall(r",", addr)) > 1:
            addr_pieces = re.search(', ([^,]+), (\w{2}) ([0-9]{5})$', addr)
        else:
            if len(re.findall(r"([0-9]{5})$", addr)) > 0:
                addr_pieces = re.search('^([^,]+), (\w{2}) ([0-9]{5})$', addr)
            else:
                addr_pieces = re.search('^([^,]+), (\w{2})$', addr)
        city = addr_pieces.group(1)
        state = addr_pieces.group(2)
    print(city,end=',')
    print(state)

    # random sleep to try and prevent Google from blocking us
    time.sleep(randint(30,60))
