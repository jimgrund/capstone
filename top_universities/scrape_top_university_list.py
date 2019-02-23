from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import re
import os

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

def scrapeUrl(universities_url):
    print("Scraping ", universities_url)
    # Firefox session
    driver = webdriver.Firefox()
    driver.get(universities_url)
    driver.implicitly_wait(50)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    code_soup = soup.find_all('div', attrs={'class': 'shadow-dark block-flush'})

    universities = []
    for i in code_soup:
        #   print(str(i.getText()))
        university_links = i.find_all('h3', attrs={'class':'heading-large block-tighter'})
        for link in university_links:
            universities.append(link.find('a'))

    # close the browser
    driver.close()

    return universities


for university_url in university_urls:
    universities = universities + scrapeUrl(university_url)

for university in universities:
    print(university)
