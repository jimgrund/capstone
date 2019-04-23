# capstone
<br/><br/>

Step 1) "top_universities" directory.  This directory is used to scrape the Top 100 universities and then attempt to identify details about the universities including which of these universities offer a masters degree program in Data Science.<br>
* scrape_top_university_list.py - *scrapes usnews.com for their top 100 universities list*
* city_state.py - *scrapes google.com search results for city and state information for the top 100 universitites*
* phone_numbers.py - *scrapes google.com search results for phone numbers of the top 100 universities*
<br/><br/>

Step 2) Manually visit the websites of the universities to confirm whether a masters in data science program exists and capture the course details within the curriculum.
<br/><br/>

Step 3) "University Course Clustering" directory.  This directory is used to identify categories for courses identified within Step 2.
* Clustering Code.py - *Uses clustering to group the university courses and determines an appropriate category for the courses*
<br/><br/>

Step 4) "Indeed Scraping" directory.  This directory is used to scrape Indeed.com to identify all job postings for data science, machine learning, NLP, etc courses within the US.
* get_urls.py - *Performs an initial search on Indeed and retrieves the listing of URLs for the jobs matching the search query*
* get_data.py - *Takes the URL listing and scrapes the job posting details from Indeed*
* clean_locations.py - *Reads the location field for each job posting and cleans the field to contain only city and state*
<br/><br/>

Step 5) "job_analysis" directory.  This directory is used to analyze the contents of the Indeed job postings and grab all named entities within the posting.
* analyze_jobs.py - *record the named entity objects within every job posting*
<br/><br/>

Step 6) "distances" directory.  This directory is used to grab the distances between every university offering a masters program and every job posting scraped from Indeed.
* distance.py - *uses Google Distance Matrix API to obtain and record the distance between every university and job post*
<br/><br/>

Step 7) "vectors" directory.  This directory is used to compute a vector similarity score of the university categories (from step 3) compared to the job posting named entities (from step 5).
* measure_vector.py - *use spaCy similarity scores to determine the relevance of the university categories to the job posting content*
<br/><br/>
