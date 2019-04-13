#!/usr/bin/env python3

import numpy as np
import spacy
from sklearn.decomposition import PCA
#nlp = spacy.load("en_core_web_lg")
#nlp = spacy.load("xx_ent_wiki_sm")
nlp = spacy.load("en_vectors_web_lg")


def GetSimilarityScore(namedEntity1, namedEntity2):
    token1=nlp(namedEntity1)
    token2=nlp(namedEntity2)
    score = token1.similarity(token2)
    #print(token1.text, token2.text, score)
    return score

def IdentifyUniversityCategory(universityCategories, jobEntities):
    last_category_score = 0
    best_category = ''

    # test each category from the university
    for category in universityCategories:
        category_score = 0
        category_scores = []

        # test each named entity from the job posting
        for entity in jobEntities:

            # get a similarity score for the current university category and current named entity
            cur_score = GetSimilarityScore(category, entity)

            # append that score to a list
            category_scores.append(cur_score)

        # take the list of scores for the current category and compute an average score 
        cur_score = sum(category_scores)/len(category_scores)

        # if we're looking for the category that best matches the job posting,
        # we only care about the category that gets the highest score
        if cur_score > category_score:
            category_score = cur_score

        # if we're looking for the category that best matches the job posting,
        # we only care about the category that gets the highest score
        print(category, category_score)
        if category_score > last_category_score:
            last_category_score = category_score
            best_category = category

    # now that we now, let's return the category assigned to job posting
    return best_category


#print(GetSimilarityScore('data scientist','NLP'))
jobEntities= [ "data", "scientist", "writing experience", "ideas", "start", "document", "minutes", "anything", "send", "software", "center", "language", "way", "textio", "way", "thousands", "companies", "scientist", "analytics", "understanding", "users", "product", "business", "role", "team", "data scientists", "engineers", "product", "managers", "others", "roadmap", "work", "insights", "power", "company", "decisions", "product direction", "quality", "impact", "textio", "features", "analysis", "workflows", "data", "products", "impact", "customers", "analyses", "influence", "behavior", "platform", "stories", "shares", "world", "welcoming", "science team", "company", "value", "place", "experiment", "data scientist", "join", "colleagues", "organization", "analytics needs", "roadmap", "design", "creation", "maintenance", "solutions", "sources", "pipelines", "product instrumentation", "metrics", "experimentation", "capabilities", "evolution", "superb", "experience", "business", "questions", "analyses", "results", "customer impact", "partners", "information", "quantify", "uncertainty", "face", "expertise", "science", "teams", "mentorship", "partnership", "leadership", "building analytics/bi", "solutions", "variety", "sources", "end", "functions", "history", "time", "growth", "problem", "spaces", "path", "clarity", "steps", "path", "business context", "contours", "data set", "skills", "exploration", "inference", "visualization", "environment", "prototypes", "specs", "pride", "things", "track record", "point", "view", "people", "diversity", "opportunity", "team", "backgrounds", "perspectives", "skills", "work", "interview experience", "philosophy", "benefits", "https", "//textio.com/careers/", "share", "story", "days", "job", "report job", "jobapply nowapply" ]

jobEntities = [ "data", "scientist", "marketing", "analytics", "reviews-lakeland", "people", "here.as", "business", "team", "marketing measurement", "behaviors", "characteristics", "customers", "measure", "purchasing behavior change", "product", "customer segment level", "sales", "methodologies", "tests", "work", "cloud", "datasets", "recommendations", "decision", "needs", "publix", "forecasting", "machine", "methods", "publix", "’", "research", "directions", "decision", "process", "customer product", "recommendations", "communications", "services", "merchandising", "customer account", "offers", "media tactics", "responsibilities", "consultation", "personalization", "customer", "interfaces", "publix", "science", "solutions", "machine learning", "intelligence", "processes", "efficiency", "results", "design", "measurement", "customer personalization", "programs", "marketing channel", "product hierarchy", "analysis", "partners", "understanding", "teams", "customer", "transaction", "campaign", "data", "trends", "patterns", "campaign performance and/or customer behavior", "systems", "data flows", "changes", "preferences", "network", "constraints", "objectives", "qualifications", "master ’", "degree", "science", "information", "systems", "computer science", "statistics", "mathematics", "economics", "finance", "field", "college", "university", "experience", "years", "computer science", "marketing", "finance", "years", "experience", "sql", "r code", "python", "syntax", "functionality", "tools", "knowledge", "databases", "data lakes", "formats", "text", "image", "sentiment", "audio/video expert knowledge", "software knowledge", "spss", "sas", "business intelligence", "sql", "basic", "enterprise manager", "intermediate knowledge", "visualization", "tableau", "desktop", "ability", "curiosity", "days", "job", "report job", "jobapply nowapply", "company" ]

    #"url": "https://www.indeed.com/rc/clk?jk=fd83355c2b23438c&fccid=77a32bcb59e7f031&vjs=3",
jobEntities = [ "enterprise", "data", "scientist", "ifarmers", "insurance", "reviews-woodland", "hills", "cafarmers", "insurance group3,905", "people", "here.we", "farmers", "join", "team", "professionals", "farmers", "skills", "job", "knowledge", "roles", "training", "opportunities", "award", "university", "magazine amongst", "units", "world", "career", "today", "scientist i", "part", "science team", "analysis", "modeling", "ualization", "services", "lines", "business", "service", "functions", "insurance group", "scientist", "end", "solutions", "part", "models", "datasets", "results", "teams", "job", "variety", "sources", "databases", "web", "files", "formats", "json", "parquet", "analysis describe", "aggregation/summarization", "build", "tools", "reports", "dashboards", "applications", "clients", "patterns", "trends", "data", "comparisons", "data points", "analysis", "reduction", "techniques", "pca", "cluste ring", "permutation", "tests", "hypothesis", "construct", "validate", "models", "techniques", "actions", "environment education", "requirements", "master", "degree", "field", "excellence", "phd", "experience", "year", "analytics", "role", "business intelligence analyst", "analyst", "skill requirement proficiency", "following", "r", "proficiency", "powerbi", "tableau", "qlikview", "d3.js", "sql", "machine learning", "glms", "cluster", "analyses", "arima", "ets", "decision", "trees", "svm", "networks", "methods", "familiarity", "management", "tools", "asana", "basecamp", "liquidplanner", "opportunity employer", "strength", "workforce", "] >", "schedule", "job posting", "days", "report job", "jobapply nowapply", "company" ]

universityCategories = [
    "Computer Science",
    "Machine Learning",
    "Statistics",
    "Topic",
    "Database",
    "Math",
    "Data Mining",
    "Data Science",
    "Visualization"
]
print(IdentifyUniversityCategory(universityCategories,jobEntities))


###################################################
###################################################
# Potential implementation?
###################################################
# read in mapping of universities to job postings
# loop on listing of universities
# for each university
#     grab categories for each university
#     loop on each category associated to university
#         loop on each job posting associated to each university
#             loop on the named entities for job posting
#                 compute similarity score between category and job postings
#             store the category score for each job posting
#         tally the job posting scores
#     tally the university category scores
#     use the total of scores to grade the university
#
###################################################
# Questions...
###################################################
# how do we tally the scores?  
# if university has 10 visualization courses and one ML course... should we weight the comparison of the "visualization" score 10x greater than "ML" score since it appears the university focuses greater on "visualization"?
###################################################
