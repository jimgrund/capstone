#!/usr/bin/env python3

import pprint
import numpy as np
import pandas as pd

university_categories = pd.read_csv("Course Data.csv")
job_category_scores = pd.read_json("job_posts_entities_categorized.json")
jobs_near_universities = pd.read_json("university_job_postings.json")

university_scores = {}

#{
#  "name": "Carnegie Mellon University",
#  "location": "Pittsburgh, PA",
#  "jobPostings": [
#    "69",
#    "128"
#  ]
#}

def ComputeScore(universityCategories, jobCategoryScores):
    #list
    #print(str(type(jobCategoryScores)))
    #pandas series
    #print(str(type(universityCategories)))

    totalScore = 0

    for category in universityCategories:
        #print(category)
        categoryScore = 0
        #next(item for item in jobCategoryScores if jobCategoryScores[category])
        #print(category, " : ", jobCategoryScores[category])
        for jobCategoryScore in jobCategoryScores:
            categoryScore = jobCategoryScore.get(category, None)
            if categoryScore is not None:
                break
        totalScore += categoryScore
        #print(category + " score: " + str(totalScore))

    return totalScore/universityCategories.size

for university in university_categories.University.unique():
    jobPostings = jobs_near_universities[jobs_near_universities["name"] == university].jobPostings.values.tolist()

    jobPostId = 0

    if len(jobPostings) > 0:
        jobPostings = jobPostings[0]
    else:
        print("skipping: " + university)
        continue

    #print(university)
    #continue
    totalJobScore = 0

    while jobPostId < len(jobPostings):
        #print("id: " + str(jobPostings[jobPostId]))
        #print(str(job_category_scores[jobPostId].CategoryScores))
        totalJobScore += ComputeScore(university_categories[university_categories.University == university]["Minor Cluster Name"],  job_category_scores[jobPostId].CategoryScores)
        jobPostId += 1

    averageJobScore = totalJobScore/len(jobPostings)

    university_scores.update({university: averageJobScore})
    #print(university + " score: " + str(averageJobScore))

pprint.pprint(university_scores)

print("\n\n")
print("Normalized:")
score=1.0/max(university_scores.values())
for k in university_scores:
  university_scores[k] = university_scores[k]*score

pprint.pprint(university_scores)
print(len(university_scores))

#print(str(jobs_near_universities[jobs_near_universities.name == "Duke"]["jobPostings"]))
#print(university_categories[university_categories.University == "Duke"]["Minor Cluster Name"].unique())
#print(str(job_category_scores[69].CategoryScores))
#print(jobs_near_universities.head())
#print(jobs_near_universities.name)
