# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 11:43:54 2019

@author: ashto
"""

import pandas as pd

#Read json file for job data
df = pd.read_json('C:/Users/ashto/Desktop/job_posts_entities_categorized.json')
df = df.transpose()
df = df.reset_index(drop=True)

#Read JSON file for job-university relationship
ju = pd.read_json('C:/Users/ashto/Desktop/job_university.json')

nju = pd.DataFrame(columns = ju.columns)

i = 0
for z, x in enumerate(ju.index):    
    for y in ju.iloc[x]['jobPostings']:
        nl = list(ju.iloc[x])
        nl[0] = y
        nju.loc[i] = nl
        i = i + 1

nju.to_csv('C:/Users/ashto/Desktop/jobUniversityIndex.csv', index=False)

df['University'] = None
    
#Minimum score cutoff (relative)
for i, dic in enumerate(df['CategoryScores']):
    cutoff = pd.Series(list(dic.values())).quantile(.75)
    top = dict((k, v) for k, v in dic.items() if v >= cutoff)
    top = list(top.keys())
    df['CategoryScores'][i] = top
    
#Create empty DataFrame
ndf = pd.DataFrame(columns = df.columns)
ndf = ndf.rename(columns = {'CategoryScores' : 'Category'})
ndf['job_id'] = None
ndf['uid'] = None

i = 0
for z, x in enumerate(df.index):    
    for y in df.iloc[x]['CategoryScores']:
        nl = list(df.iloc[x])
        nl[0] = y
        nl.append(z)
        nl.append(i)
        ndf.loc[i] = nl
        i = i + 1

ndf = ndf['Category', 'City', 'State', 'entities', 'location', 'posting', 'salary', 'title', 'url', 'job_id', 'uid', 'University']

ndf = ndf[ndf['Category'] != 'Other']

ndf.to_csv('C:/Users/ashto/Desktop/jobData.csv', index=False)




