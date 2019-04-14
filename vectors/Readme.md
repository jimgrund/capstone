Currently using en_vectors_web_lg Corpus
https://github.com/explosion/spacy-models/releases/tag/en_vectors_web_lg-2.1.0
python3 -m spacy download en_vectors_web_lg

measure_vectors.py reads job_posts_entities.json and measures the named entities of each job post
compared to the 9 categories used in the classification of the university course programs.
With these measurements it assigns one of the categories to the job posting and outputs 
job_posts_entities_categorized.json which includes a Category column for each job post.

Also tested with Wikipedia Corpus
https://github.com/explosion/spacy-models/releases/tag/xx_ent_wiki_sm-2.1.0
python3 -m spacy download xx_ent_wiki_sm
