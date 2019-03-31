# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 14:26:07 2019

@author: ashto
"""

from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pandas as pd

stop_words = set(stopwords.words('english')) 

xls = pd.ExcelFile('''Excel Workbook Location''')

xls.sheet_names

# to read all sheets to a map
df_map = {}
for sheet_name in xls.sheet_names:
    df_map[sheet_name] = xls.parse(sheet_name, header=None)
    
df_map

dfs = []
for i in df_map:
    df = df_map.get(i)
    df[3] = i
    dfs.append(df)

courses = pd.concat(dfs)
courses = courses.dropna(how='any')
courses.columns = ['Course ID', 'Course Title', 'Course Description', 'University']

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(list(courses['Course Title']))

true_k = 100
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=10000, n_init=10)
model.fit(X)

order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()

courses['Cluster'] = ''
courses = courses.reset_index(drop=True)

for course in courses.index:
    Y = vectorizer.transform([courses['Course Title'].iloc[course]])
    prediction = model.predict(Y)[0]
    courses['Cluster'].iloc[course] = prediction

titles = []
for i in range(true_k):
    title = courses[courses['Cluster'] == i]['Course Title']
    title = title.str.cat(sep=' ')
    word_tokens = word_tokenize(title)
    title = [w.lower() for w in word_tokens if not w in stop_words]
    ' '.join(title)
    titles.append(title)

courses['Cluster Name'] = ''
courses = courses.reset_index(drop=True)

#This must be done manually
for course in courses.index:
    if courses.iloc[course]['Cluster']  == 0:
        courses['Cluster Name'].iloc[course] = 'Machine Learning'
    if courses.iloc[course]['Cluster']  == 1:
        courses['Cluster Name'].iloc[course] = 'General Data Science'
    if courses.iloc[course]['Cluster']  == 2:
        courses['Cluster Name'].iloc[course] = 'Statistics and Probability'
    if courses.iloc[course]['Cluster']  == 3:
        courses['Cluster Name'].iloc[course] = 'Statistical Learning'
    if courses.iloc[course]['Cluster']  == 4:
        courses['Cluster Name'].iloc[course] = 'Linear Algebra'
    if courses.iloc[course]['Cluster']  == 5:
        courses['Cluster Name'].iloc[course] = 'Big Data'
    if courses.iloc[course]['Cluster']  == 6:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 7:
        courses['Cluster Name'].iloc[course] = 'Artifical Intelligence'
    if courses.iloc[course]['Cluster']  == 8:
        courses['Cluster Name'].iloc[course] = 'Time Series'
    if courses.iloc[course]['Cluster']  == 9:
        courses['Cluster Name'].iloc[course] = 'Multivariate Analysis'
    if courses.iloc[course]['Cluster']  == 10:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 11:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 12:
        courses['Cluster Name'].iloc[course] = 'Computer Vision'
    if courses.iloc[course]['Cluster']  == 13:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 14:
        courses['Cluster Name'].iloc[course] = 'Stochastic Processes'
    if courses.iloc[course]['Cluster']  == 15:
        courses['Cluster Name'].iloc[course] = 'Physics'
    if courses.iloc[course]['Cluster']  == 16:
        courses['Cluster Name'].iloc[course] = 'Statistics'
    if courses.iloc[course]['Cluster']  == 17:
        courses['Cluster Name'].iloc[course] = 'Algorithms'
    if courses.iloc[course]['Cluster']  == 18:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 19:
        courses['Cluster Name'].iloc[course] = 'Marketing'
    if courses.iloc[course]['Cluster']  == 20:
        courses['Cluster Name'].iloc[course] = 'Cloud Computing'
    if courses.iloc[course]['Cluster']  == 21:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 22:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 23:
        courses['Cluster Name'].iloc[course] = 'Programming'
    if courses.iloc[course]['Cluster']  == 24:
        courses['Cluster Name'].iloc[course] = 'Capstone'
    if courses.iloc[course]['Cluster']  == 25:
        courses['Cluster Name'].iloc[course] = 'Econometrics'
    if courses.iloc[course]['Cluster']  == 26:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 27:
        courses['Cluster Name'].iloc[course] = 'Databases'
    if courses.iloc[course]['Cluster']  == 28:
        courses['Cluster Name'].iloc[course] = 'Practicum'
    if courses.iloc[course]['Cluster']  == 29:
        courses['Cluster Name'].iloc[course] = 'Data Modeling'
    if courses.iloc[course]['Cluster']  == 30:
        courses['Cluster Name'].iloc[course] = 'Capstone'
    if courses.iloc[course]['Cluster']  == 31:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 32:
        courses['Cluster Name'].iloc[course] = 'Data Management'
    if courses.iloc[course]['Cluster']  == 33:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 34:
        courses['Cluster Name'].iloc[course] = 'Information Retrieval'
    if courses.iloc[course]['Cluster']  == 35:
        courses['Cluster Name'].iloc[course] = 'Statistical Learning'
    if courses.iloc[course]['Cluster']  == 36:
        courses['Cluster Name'].iloc[course] = 'Multivariate Statistics'
    if courses.iloc[course]['Cluster']  == 37:
        courses['Cluster Name'].iloc[course] = 'Computational Data Science'
    if courses.iloc[course]['Cluster']  == 38:
        courses['Cluster Name'].iloc[course] = 'Human-Computer Interation'
    if courses.iloc[course]['Cluster']  == 39:
        courses['Cluster Name'].iloc[course] = 'Numerical Analysis'
    if courses.iloc[course]['Cluster']  == 40:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 41:
        courses['Cluster Name'].iloc[course] = 'Statistics and Probability'
    if courses.iloc[course]['Cluster']  == 42:
        courses['Cluster Name'].iloc[course] = 'Biostatistics'
    if courses.iloc[course]['Cluster']  == 43:
        courses['Cluster Name'].iloc[course] = 'Independent Study'
    if courses.iloc[course]['Cluster']  == 44:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 45:
        courses['Cluster Name'].iloc[course] = 'Differential Equations'
    if courses.iloc[course]['Cluster']  == 46:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 47:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 48:
        courses['Cluster Name'].iloc[course] = 'Special Topics'
    if courses.iloc[course]['Cluster']  == 49:
        courses['Cluster Name'].iloc[course] = 'High Performance Computing'
    if courses.iloc[course]['Cluster']  == 50:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 51:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 52:
        courses['Cluster Name'].iloc[course] = 'Distributed Computing'
    if courses.iloc[course]['Cluster']  == 53:
        courses['Cluster Name'].iloc[course] = 'Statistics and Probability'
    if courses.iloc[course]['Cluster']  == 54:
        courses['Cluster Name'].iloc[course] = 'Software'
    if courses.iloc[course]['Cluster']  == 55:
        courses['Cluster Name'].iloc[course] = 'Research'
    if courses.iloc[course]['Cluster']  == 56:
        courses['Cluster Name'].iloc[course] = 'Mathematical Statistics and Modeling'
    if courses.iloc[course]['Cluster']  == 57:
        courses['Cluster Name'].iloc[course] = 'Vizualization'
    if courses.iloc[course]['Cluster']  == 58:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 59:
        courses['Cluster Name'].iloc[course] = 'Database Organization/Mangement'
    if courses.iloc[course]['Cluster']  == 60:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 61:
        courses['Cluster Name'].iloc[course] = 'Algorithms'
    if courses.iloc[course]['Cluster']  == 62:
        courses['Cluster Name'].iloc[course] = 'Linear Models'
    if courses.iloc[course]['Cluster']  == 63:
        courses['Cluster Name'].iloc[course] = 'Foundations'
    if courses.iloc[course]['Cluster']  == 64:
        courses['Cluster Name'].iloc[course] = 'Data Warehousing'
    if courses.iloc[course]['Cluster']  == 65:
        courses['Cluster Name'].iloc[course] = 'Time Series/Seminar Series'
    if courses.iloc[course]['Cluster']  == 66:
        courses['Cluster Name'].iloc[course] = 'Calculus'
    if courses.iloc[course]['Cluster']  == 67:
        courses['Cluster Name'].iloc[course] = 'Bayesian Statistics'
    if courses.iloc[course]['Cluster']  == 68:
        courses['Cluster Name'].iloc[course] = 'Economics'
    if courses.iloc[course]['Cluster']  == 69:
        courses['Cluster Name'].iloc[course] = 'Data Mining'
    if courses.iloc[course]['Cluster']  == 70:
        courses['Cluster Name'].iloc[course] = 'Estimation'
    if courses.iloc[course]['Cluster']  == 71:
        courses['Cluster Name'].iloc[course] = 'Data Mangement/Program Management'
    if courses.iloc[course]['Cluster']  == 72:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 73:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 74:
        courses['Cluster Name'].iloc[course] = 'Economics'
    if courses.iloc[course]['Cluster']  == 75:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 76:
        courses['Cluster Name'].iloc[course] = 'Artifical Intelligence'
    if courses.iloc[course]['Cluster']  == 77:
        courses['Cluster Name'].iloc[course] = 'Regression Analysis'
    if courses.iloc[course]['Cluster']  == 78:
        courses['Cluster Name'].iloc[course] = 'Causal Inference'
    if courses.iloc[course]['Cluster']  == 79:
        courses['Cluster Name'].iloc[course] = 'Optimization'
    if courses.iloc[course]['Cluster']  == 80:
        courses['Cluster Name'].iloc[course] = 'Bioinformatics'
    if courses.iloc[course]['Cluster']  == 81:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 82:
        courses['Cluster Name'].iloc[course] = 'Survey Methods/Analysis'
    if courses.iloc[course]['Cluster']  == 83:
        courses['Cluster Name'].iloc[course] = 'Behavior'
    if courses.iloc[course]['Cluster']  == 84:
        courses['Cluster Name'].iloc[course] = 'Databases'
    if courses.iloc[course]['Cluster']  == 85:
        courses['Cluster Name'].iloc[course] = 'Data Security'
    if courses.iloc[course]['Cluster']  == 86:
        courses['Cluster Name'].iloc[course] = 'Computational Learning Theory'
    if courses.iloc[course]['Cluster']  == 87:
        courses['Cluster Name'].iloc[course] = 'Monte Carlo'
    if courses.iloc[course]['Cluster']  == 88:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 89:
        courses['Cluster Name'].iloc[course] = 'Data Mining'
    if courses.iloc[course]['Cluster']  == 90:
        courses['Cluster Name'].iloc[course] = 'Big Data'
    if courses.iloc[course]['Cluster']  == 91:
        courses['Cluster Name'].iloc[course] = 'Tools for Data Science'
    if courses.iloc[course]['Cluster']  == 92:
        courses['Cluster Name'].iloc[course] = 'NLP'
    if courses.iloc[course]['Cluster']  == 93:
        courses['Cluster Name'].iloc[course] = 'Decision Making'
    if courses.iloc[course]['Cluster']  == 94:
        courses['Cluster Name'].iloc[course] = 'Statistical Methods'
    if courses.iloc[course]['Cluster']  == 95:
        courses['Cluster Name'].iloc[course] = 'Deep Learning'
    if courses.iloc[course]['Cluster']  == 96:
        courses['Cluster Name'].iloc[course] = 'Reclassify'
    if courses.iloc[course]['Cluster']  == 97:
        courses['Cluster Name'].iloc[course] = 'Predictive Analytics'
    if courses.iloc[course]['Cluster']  == 98:
        courses['Cluster Name'].iloc[course] = 'Political Science'
    if courses.iloc[course]['Cluster']  == 99:
        courses['Cluster Name'].iloc[course] = 'Python Programming'

backup = courses

numClusters = len(courses.groupby('Cluster Name').count())
classed = courses[courses['Cluster Name'] != 'Reclassify'].reset_index(drop=True)
reclass = courses[courses['Cluster Name'] == 'Reclassify'].reset_index(drop=True)

X = vectorizer.fit_transform(list(classed['Course Title']))

model = KMeans(n_clusters=numClusters, init='k-means++', max_iter=10000, n_init=10)
model.fit(X)

for course in reclass.index:
    Y = vectorizer.transform([reclass['Course Title'].iloc[course]])
    prediction = model.predict(Y)[0]
    reclass['Cluster'].iloc[course] = prediction

#This must be done manually
for course in reclass.index:
    if reclass.iloc[course]['Cluster']  == 5:
        reclass['Cluster Name'].iloc[course] = 'Programming'
    if reclass.iloc[course]['Cluster']  == 7:
        reclass['Cluster Name'].iloc[course] = 'Data Mining'
    if reclass.iloc[course]['Cluster']  == 8:
        reclass['Cluster Name'].iloc[course] = 'Databases'
    if reclass.iloc[course]['Cluster']  == 30:
        reclass['Cluster Name'].iloc[course] = 'Statistics'
    if reclass.iloc[course]['Cluster']  == 33:
        reclass['Cluster Name'].iloc[course] = 'Algorithms'
    if reclass.iloc[course]['Cluster']  == 39:
        reclass['Cluster Name'].iloc[course] = 'Computer and Network Security' 
    if reclass.iloc[course]['Cluster']  == 46:
        reclass['Cluster Name'].iloc[course] = 'Special Topics' 
    if reclass.iloc[course]['Cluster']  == 39:
        reclass['Cluster Name'].iloc[course] = 'Computer and Network Security'     

classed = pd.concat([classed, reclass[reclass['Cluster Name'] != 'Reclassify'].reset_index(drop=True)], axis=0)
unclassed = reclass[reclass['Cluster Name'] == 'Reclassify'].reset_index(drop=True)

for course in unclassed.index:
    unclassed['Cluster Name'].iloc[course] = 'Special Elective'
