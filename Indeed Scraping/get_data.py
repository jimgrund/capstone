#Packages

import requests
import json
from bs4 import BeautifulSoup

#Setup

##Ashton: Added load of urls.txt file
query = (['data+scientist'])[0]
with open('urls.txt') as f:
    urls = json.load(f)

def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    return soup

def extract_salary_from_result(soup):
  salaries = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
    try:
      salaries.append(div.find('nobr').text)
    except:
      try:
        div_two = div.find(name="div", attrs={"class":"sjcl"})
        div_three = div_two.find("div")
        salaries.append(div_three.text.strip())
      except:
        salaries.append("Nothing_found")
  return(salaries)

def get_posting(url):
    # Get the url content as BS object
    soup = get_soup(url)
    
    # The job title is held in the h3 tag
    title = soup.find(name='h3').getText().lower()
    location_obj = soup.find(name='div', attrs={'class': "jobsearch-InlineCompanyRating"})
    if location_obj:
        location = location_obj.get_text()
    else:
        location = "" 
    salary = extract_salary_from_result(soup)
    posting = soup.find(name='div', attrs={'class': "jobsearch-JobComponent"}).get_text()

    return title, location, salary, posting.lower()

    ##Ashton: Removed unneeded code. 

def get_data(query, urls):
    ##Ashton: removed unneeded code
    
    postings_dict = {}

    #Continue only if the requested number of pages is valid (when invalid, a number is returned instead of list)
    if isinstance(urls, list):
        num_urls = len(urls)
        for i, url in enumerate(urls):
            try:
                title, location, salary, posting = get_posting(url)
                postings_dict[i] = {}
                postings_dict[i]['title'], postings_dict[i]['location'], postings_dict[i]['salary'], postings_dict[i]['posting'], postings_dict[i]['url'] = \
                    title, location, salary, posting, url
            except Exception as e:
                print("failed URL, moving on" + e)
                continue
        
        ##Ashton: changed name of json file
        # Save the dict as json file
        file_name = query.replace('+', '_') + '.data'
        with open(file_name, 'w') as f:
            json.dump(postings_dict, f)

        print('All {} postings have been scraped and saved!'.format(num_urls))
    else:
        print("Due to similar results, maximum number of pages is only {}. Please try again!".format(urls))

get_data(query, urls)
