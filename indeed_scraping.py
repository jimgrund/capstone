import re
import json
from bs4 import BeautifulSoup
from selenium import webdriver

# Setup

job_query = (['data+scientist', 'machine+learning+engineer'])
cities = (['New+York','Chicago','San+Francisco', 'San+Diego', 'Austin', 'Seattle', 'Los+Angeles', 'Philadelphia', 'Atlanta', 'Dallas', 'Pittsburgh', 'Portland', 'Phoenix', 'Denver', 'Houston', 'Miami', 'Washington+DC', 'Boston'])
x = (['data+scientist'])
y = (['Washington+DC', 'Boston'])
#columns = ["url", "job_title", "city", "salary", "summary"]
#sample_df = pd.DataFrame(columns = columns)

# Code

def get_soup(url):
    driver = webdriver.Chrome(executable_path='/Users/alexa/Desktop/Capstone/chromedriver')
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    driver.close()
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
def get_urls(query, num_pages):
    # We always need the first page
    #base_url = 'https://www.indeed.com/jobs?q={}&l={}'.format(query, location)
    base_url = 'https://www.indeed.com/jobs?as_and&as_phr={}&as_any&as_not&as_ttl&as_cmp&jt=fulltime&st&as_src&salary&radius=25&l&fromage=30&limit=50&sort&psf=advsrch&vjk=f7877e10f05da061'.format(query)
    soup = get_soup(base_url)
    urls = grab_job_links(soup)

    # Get the total number of postings found
    posting_count_string = soup.find(name='div', attrs={'id': "searchCount"}).get_text()
    posting_count_string = posting_count_string[posting_count_string.find('of') + 2:].strip()
    # print('posting_count_string: {}'.format(posting_count_string))
    # print('type is: {}'.format(type(posting_count_string)))

    try:
        posting_count = int(posting_count_string)
    except ValueError:  # deal with special case when parsed string is "360 jobs"
        posting_count = int(re.search('\d+', posting_count_string).group(0))
        # print('posting_count: {}'.format(posting_count))
        # print('\ntype: {}'.format(type(posting_count)))
    finally:
        posting_count = 330  # setting to 330 when unable to get the total
        pass

    # Limit nunmber of pages to get
    max_pages = round(posting_count / 10) - 3
    if num_pages > max_pages:
        print('returning max_pages!!')
        return max_pages

        # Additional work is needed when more than 1 page is requested
    if num_pages >= 2:
        # Start loop from page 2 since page 1 has been dealt with above
        for i in range(2, num_pages + 1):
            num = (i - 1) * 50 # start new search page at increments of 50
            #base_url = 'https://www.indeed.com/jobs?q={}&l={}&start={}'.format(query, location, num)
            base_url = 'https://www.indeed.com/jobs?as_and&as_phr={}&as_any&as_not&as_ttl&as_cmp&jt=fulltime&st&as_src&salary&radius=25&l&fromage=30&limit=50&start={}&sort&psf=advsrch&vjk=f7877e10f05da061'.format(query, num)
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
    location = soup.find(name='div', attrs={'class': "jobsearch-InlineCompanyRating"}).get_text()
    salary = extract_salary_from_result(soup)
    posting = soup.find(name='div', attrs={'class': "jobsearch-JobComponent"}).get_text()

    return title, location, salary, posting.lower()

    # if 'data scientist' in title:  # We'll proceed to grab the job posting text if the title is correct
    # All the text info is contained in the div element with the below class, extract the text.
    # posting = soup.find(name='div', attrs={'class': "jobsearch-JobComponent"}).get_text()
    # return title, posting.lower()
    # else:
    # return False

    # Get rid of numbers and symbols other than given
    # text = re.sub("[^a-zA-Z'+#&]", " ", text)
    # Convert to lower case and split to list and then set
    # text = text.lower().strip()

    # return text


def get_data(query, num_pages, location):
    # Convert the queried title to Indeed format
    query = '+'.join(query.lower().split())

    postings_dict = {}
    urls = get_urls(query, num_pages, location)

    #  Continue only if the requested number of pages is valid (when invalid, a number is returned instead of list)
    if isinstance(urls, list):
        num_urls = len(urls)
        for i, url in enumerate(urls):
            try:
                title, location, salary, posting = get_posting(url)
                postings_dict[i] = {}
                postings_dict[i]['title'], postings_dict[i]['location'], postings_dict[i]['salary'], postings_dict[i]['posting'], postings_dict[i]['url'] = \
                    title, location, salary, posting, url
            except:
                continue

        # Save the dict as json file
        file_name = query.replace('+', '_') + 'json'
        with open(file_name, 'w') as f:
            json.dump(postings_dict, f)

        print('All {} postings have been scraped and saved!'.format(num_urls))
        # return postings_dict
    else:
        print("Due to similar results, maximum number of pages is only {}. Please try again!".format(urls))

# Run Code

get_urls("data+scientist", 18)

# Check for duplicates in urls.txt
f = open("urls.txt", "r")
c = f.read()

def remove(duplicate):
    final_list = []
    for i in duplicate:
        if i not in final_list:
            final_list.append(i)
    return final_list

remove(c)
print(len(c))




