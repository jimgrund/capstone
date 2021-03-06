#Packages

import re
import requests
import json
from bs4 import BeautifulSoup

#Setup

job_query = (['data+scientist'])

#Code

def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    return soup

def grab_job_links(soup):
    urls = []
    # Loop thru all the posting links
    for link in soup.find_all('h2', {'class': 'jobtitle'}):
        # Since sponsored job postings are represented by "a target" instead of "a href", no need to worry here
        partial_url = link.a.get('href')
        # This is a partial url, we need to attach the prefix
        url = 'https://www.indeed.com' + partial_url
        # Make sure this is not a sponsored posting
        urls.append(url)
    return urls

#def get_urls(query, num_pages, location):
def get_urls(query):
    # We always need the first page
    
    ##Ashton: chagned URL. Was directing to specific job posting. Now goes to search page
    base_url = 'https://www.indeed.com/jobs?as_and=&as_phr={}&as_any=&as_not=&as_ttl=&as_cmp=&jt=fulltime&st=&as_src=&salary=&radius=25&l=&fromage=30&limit=50&sort=&psf=advsrch'.format(query)
    soup = get_soup(base_url)
    urls = grab_job_links(soup)

    # Get the total number of postings found
    posting_count_string = soup.find(name='div', attrs={'id': "searchCount"}).get_text()
    posting_count_string = posting_count_string[posting_count_string.find('of') + 2:].strip()
    ##Ashton: Changed strip of number of job postings. Was forcing posting_count to default to 330
    ##Original strip pulled 'x jobs' instead of 'x'
    posting_count_string = ''.join(i for i in posting_count_string if i.isdigit())
    
    try:
        posting_count = int(posting_count_string)
    except ValueError:  # deal with special case when parsed string is "360 jobs"
        posting_count = int(re.search('\d+', posting_count_string).group(0))
        # print('posting_count: {}'.format(posting_count))
        # print('\ntype: {}'.format(type(posting_count)))
    
    ##Ashton: changed 10 to 50 as there are now 50 results per page instead of 10
    num_pages = round(posting_count / 50) - 3

        # Additional work is needed when more than 1 page is requested
    if num_pages >= 2:
        # Start loop from page 2 since page 1 has been dealt with above
        for i in range(2, num_pages + 1):
            num = (i - 1) * 50 # start new search page at increments of 50
            
            ##Changed URL again
            base_url = 'https://www.indeed.com/jobs?as_and=&as_phr={}&as_any=&as_not=&as_ttl=&as_cmp=&jt=fulltime&st=&as_src=&salary=&radius=25&l=&fromage=30&limit=50&start={}&sort=&psf=advsrch'.format(query, num)
            
            try:
                soup = get_soup(base_url)
                # We always combine the results back to the list
                urls += grab_job_links(soup)
            except:
                continue

    # Check to ensure the number of urls gotten is correct
    # assert len(urls) == num_pages * 10, "There are missing job links, check code!"

    #return urls
    with open('urls.txt', 'w') as f:
        json.dump(urls, f)

##Ashton: Changed number of searches

get_urls("data+scientist")

# Check for duplicates in urls.txt

##Ashton: Changed load from read txt to read json. Was causing error in remove
##duplicates function as for loop looked at letters of string individually
with open('urls.txt') as f:
    data = json.load(f)

def remove(duplicate):
    final_list = []
    for i in duplicate:
        if i not in final_list:
            final_list.append(i)
    return final_list

remove(data)
print(len(data))

##Ashton: Rewrite the old txt file to include only unique URLs.
with open('urls.txt', 'w') as f:
    json.dump(data, f)
