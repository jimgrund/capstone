#!/usr/bin/env python

# this scriptlette is used to clean the location fields of the json obtained from scraping Indeed.com
# we only wanted the city,state component found in the location field of the json

import json
import re

ds_filehandle = open('data_scientist.json')
ds_str        = ds_filehandle.read()
ds_data       = json.loads(ds_str)

for job_post in range(len(ds_data)):
    try:
        print(ds_data[str(job_post)]['location'])
        m = re.search(r'-([^-\d]+)\d*\-*\d*$', ds_data[str(job_post)]['location'])
        print("\t",m.group(1))
        ds_data[str(job_post)]['location'] = m.group(1)
    except:
        print("\tnothing to regex")
        try:
            ds_data[str(job_post)]['location'] = ""
        except:
            print("failed to null out value")


with open('cleansed_job_posts.json', 'w') as clean_ds_filehandle:
    json.dump(ds_data, clean_ds_filehandle)
