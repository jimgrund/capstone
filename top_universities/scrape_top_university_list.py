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
                   'https://www.usnews.com/best-colleges/rankings/national-universities?_page=10'
                  ]

# placeholder to store the top N universities
universities = []

def firstGoogleResult(query_url):
    # Firefox session
    driver = webdriver.Firefox()
    driver.get(query_url)
    driver.implicitly_wait(20)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    code_soup = soup.find_all('div', attrs={'class': 'srg'})

    # print("Code Soup: " + str(code_soup))

    search_results = []
    for i in code_soup:
        #   print(str(i.getText()))
        result_links = i.find_all('div', attrs={'class':'r'})
        # print("Result Links: " + str(result_links))
        for link in result_links:
            # print(str(link))
            search_results.append(link.find('a')['href'])

    # random sleep to try and prevent Google from blocking us
    time.sleep(randint(20,60))

    # close the browser
    driver.close()

    # return the first result if results are obtained..
    if (len(search_results) > 0):
        return search_results[0]

    # else return empty string
    return ''


def googleUniversity(university_name):
    query_string = '"'+university_name+'" "data science" "master program" "site:edu"'
    query_string = urllib.parse.quote_plus(query_string)
    google_query_url = 'https://www.google.com/search?q='+query_string
    #print(google_query_url)
    return firstGoogleResult(google_query_url)

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


for university in universities:
    print(university.rstrip(),end=',')
    print(googleUniversity(university))
