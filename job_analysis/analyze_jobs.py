#!/usr/bin/env python

import pandas as pd
import json
import gensim
import nltk
from gensim import corpora, models
from nltk.stem import WordNetLemmatizer, SnowballStemmer



#   "4": {
#     "title": "data scientist",
#     "location": "Charlotte, NC",
#     "salary": [],
#     "posting": "data scientistastral technologies inc-charlotte, nc$60,000 - $75,000 a yearastral techs is searching for a data scientist, who will be responsible for the critical data scientist initiatives. you work will include the application of machine learning techniques to modeling, data mining and statistical analyses that push limits of performance and efficiency. you will also be responsible for writing, deploying, and maintaining production grade python code.what you'll do:work closely with data scientists on all stages of new model development: data exploration, feature generation and model training using the most advanced tools in the spacesupport and optimize existing models by identifying new data sources and generating novel featurescollaborate with teams across the company: business operations, marketing, finance and riskcommunicate key results to senior management in verbal, visual, and written mediaown the implementation of your models and insights and see them deliver real resultswhat we look for:bachelors degree in computer science, statistics, mathematics, information systems or equivalent technical degree0-2 years of hands-on experience as a data scientist, machine learning engineer or a comparable analytical position0-2 years of hands-on experience with python and the supporting analysis libraries/ecosysteman excellent understanding of both traditional statistical modeling and machine learning techniques and algorithms: regression, clustering, ensembling (random forest, gradient boosting), deep learning (neural networks), etcproficiency with python and sqlfamiliarity with git and linux/os command lineself-starter - excited to learn unfamiliar concepts on the jobdelivery-oriented approachability to get things done within a strict time frame/ability to juggle multiple assignmentsdeep interest in learning both the theoretical and practical aspects of working with and deriving insights from datagreat communication skillsnice to havemasters degree in computer science, statistics, mathematics, information systems or equivalentelectives in data science related subjectsinsight into python programming & sql skillsjob type: full-timesalary: $60,000.00 to $75,000.00 /yeareducation:master's (required)work authorization:united states (required)4 days ago - save job - report jobif you require alternative methods of application or screening, you must approach the employer directly to request this as indeed is not responsible for the employer's application process.apply nowapply nowsave this job",
#     "url": "https://www.indeed.com/company/Astral-Technologies-Inc/jobs/Data-Scientist-3b717c274029b71e?fccid=617bbc89cc6cb59e&vjs=3"
#   },


def get_entities(text):
    sentences = nltk.tokenize.sent_tokenize(text)
    tokens = [nltk.tokenize.word_tokenize(s) for s in sentences]
    pos_tagged_tokens = [nltk.pos_tag(t) for t in tokens]
    pos_tagged_tokens = [token for sent in pos_tagged_tokens for token in sent]

    all_entity_chunks = []
    previous_pos = None
    current_entity_chunk = []
    for (token, pos) in pos_tagged_tokens:

        if pos == previous_pos and pos.startswith('NN'):
            current_entity_chunk.append(token)
        elif pos.startswith('NN'):
            if current_entity_chunk != []:

                # Note that current_entity_chunk could be a duplicate when appended,
                # so frequency analysis again becomes a consideration

                all_entity_chunks.append((' '.join(current_entity_chunk), pos))
            current_entity_chunk = [token]

        previous_pos = pos

    # Store the chunks as an index for the document
    # and account for frequency while we're at it...

    post_entities = {}
    for c in all_entity_chunks:
        post_entities[c] = post_entities.get(c, 0) + 1


    proper_nouns = []

    #for (entity, pos) in post_entities:
    #    print('\t%s (%s)' % (entity, post_entities[(entity, pos)]))

    return(list(list(zip(*post_entities))[0]))


def get_topics(text):
    def lemmatize_stemming(text):
        stemmer = SnowballStemmer("english", ignore_stopwords=True)
        return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

    def preprocess(text):
        result = []
        for token in gensim.utils.simple_preprocess(text):
            if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
                #result.append(token)
                result.append(lemmatize_stemming(token))
        return result

    words = []
    for word in text.split(' '):
        words.append(word)

    processed_data = preprocess(text)

    dictionary = gensim.corpora.Dictionary([processed_data])

    bow_corpus = [dictionary.doc2bow(processed_data)]

    bow_doc_0 = bow_corpus[0]

    tfidf = models.TfidfModel(bow_corpus)

    corpus_tfidf = tfidf[bow_corpus]

    # LDA Model using Bag of Words
    lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=15, id2word=dictionary, passes=2, workers=4)

    topic_score_list = lda_model.show_topics(num_topics=1, num_words=15, log=False, formatted=False)[0][1]
    topics_list = [topic[0] for topic in topic_score_list]
    return(topics_list)
    #return(lda_model.show_topics(num_topics=1, num_words=15, log=False, formatted=False)[0][1])




with open('cleansed_job_posts.json', 'r') as jobs_filehandle:
    jobs_data = json.load(jobs_filehandle)
    for job_id in jobs_data.keys():
        print(job_id)
        #print('Posting: ' + jobs_data[job_id]['posting'])
        print('URL: ' + jobs_data[job_id]['url'])
        print("TOPICS BEGIN")
        #print(get_topics(jobs_data[job_id]['posting']))
        print(get_entities(jobs_data[job_id]['posting']))
        jobs_data[job_id]['entities'] = get_entities(jobs_data[job_id]['posting'])
        print("TOPICS END")
        print('')
        print('')

with open('job_posts_entities.json', 'w') as posts_entities_filehandle:
    json.dump(jobs_data, posts_entities_filehandle)

