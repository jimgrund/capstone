#!/usr/bin/env python

####
## Reads in cleansed jobs data file
## and university listing that defines City, State, and Has DS MS columns
## Requires GoogleMaps API key
##
## Outputs json file that is a mapping between university and jobs within given radius (in miles)
####

import googlemaps
import pandas as pd
import csv
import json
import re
import time
import os

# google maps api key with distance matrix feature activated
GOOGLE_KEY = 'XXXXX'

# radius in miles around university to look for jobs
RADIUS = 150

# convert radius to meters
RADIUS_IN_METERS = (RADIUS * 1609)

gmaps = googlemaps.Client(key=GOOGLE_KEY)

# initialize a cache of distances between cities
distanceCache = {}

# lookup the distance via the google maps api
def GetGoogleDistance(city1,city2):
    # google distance matrix returns in meters
    # 1609 meters per mile

    # sleep for a very brief moment to not max out google api limit
    time.sleep(0.001)

    # grab only the distance value which is in meters
    distance = gmaps.distance_matrix(city1, city2, units='imperial')['rows'][0]['elements'][0]['distance']['value']
    return distance


# check the local cache for distance data
def CheckCachedDistance(city1,city2):
    if city1 in distanceCache:
        if city2 in distanceCache[city1]:
            return distanceCache[city1][city2]
    if city2 in distanceCache:
        if city1 in distanceCache[city2]:
            return distanceCache[city2][city1]
    return None


# append distance data into local cache for future lookups
def CacheDistance(city1,city2,distance):
    if city1 not in distanceCache:
        distanceCache[city1] = {}
    distanceCache[city1][city2] = distance

    # write the cache out to disk in case we crash
    SaveDistanceCache()


# lowercase and remove leading and trailing whitespace
def CleanCity(city):
    city = city.lower()
    city = city.lstrip()
    city = city.rstrip()
    return city


# get the distance between two cities
# checking both cached data and lookup via google api
def GetDistance(city1,city2):
    # clean and normalize cities
    city1 = CleanCity(city1)
    city2 = CleanCity(city2)

    cachedDistance = CheckCachedDistance(city1,city2)
    if cachedDistance is not None:
        return cachedDistance
    else:
        googleDistance = GetGoogleDistance(city1,city2)
        CacheDistance(city1,city2,googleDistance)
        return googleDistance


def GetJobsNearCity(city):
    # initialize jobs_list
    jobsList = []

    # read in the job posting data for distance calculation
    with open('cleansed_job_posts.json', 'r') as jobsFilehandle:
        jobsData = json.load(jobsFilehandle)

        # loop over each of the job ids in the data
        for jobId in jobsData.keys():
            # print output for debugging and tracking purposes
            print(jobId)
            #print('URL: ' + jobsData[jobId]['url'])
            jobCity = jobsData[jobId]['location']

            # if jobCity is blank or doesn't include a comma, continue to next job posting
            # exclude HI as well
            if jobCity == "" or not re.match('.+,.+', jobCity) or re.match('.+, *HI *', jobCity):
                continue

            # if distance is within defined radius, add to the list of jobs to return for this request
            if GetDistance(city, jobCity) <= RADIUS_IN_METERS:
                jobsList.append(jobId)

        jobsFilehandle.close()
        return(jobsList)
        

def SaveDistanceCache():
    with open('distanceCache.json', 'w') as fh:
        json.dump(distanceCache, fh)

def LoadDistanceCache():
    if os.path.isfile('distanceCache.json'):
        with open('distanceCache.json', 'r') as fh:
            distanceCache = json.load(fh)
    else:
        distanceCache = {}
    return distanceCache

universities = []
universityIndex = 0

distanceCache = LoadDistanceCache()

# read in the university data for distance calculation
with open('universities.csv', 'r') as universities_filehandle:
    universities_reader = csv.DictReader(universities_filehandle)
    for row in universities_reader:
        if row['Has DS MS'].lower() == "yes":
            university = {}
            universityCity = row['City'] + ", " + row['State']
            print(str(universityIndex) + " " + row['University'] + " " + universityCity)
            jobPostings = GetJobsNearCity(universityCity)
            university['name']         = row['University']
            university['location']     = universityCity
            university['jobPostings']  = jobPostings
            universities.append(university)
            universityIndex += 1


# write modified dataframe out to new json file
with open('university_job_postings.json', 'w') as university_job_postings_filehandle:
    json.dump(universities, university_job_postings_filehandle)

SaveDistanceCache()
