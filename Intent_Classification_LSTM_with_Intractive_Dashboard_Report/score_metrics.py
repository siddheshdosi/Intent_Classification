# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 17:55:02 2021

@author: Siddhesh.Dosi
"""
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
import pandas as pd
from sklearn.metrics import confusion_matrix,classification_report,accuracy_score

def tfidf_score(corpus,ngram_range=(1,1)):
    vectorizer = TfidfVectorizer(analyzer='word', ngram_range=ngram_range)
    vz = vectorizer.fit_transform(corpus)
    tfidf = dict(zip(vectorizer.get_feature_names(), vectorizer.idf_))
    tfidf = pd.DataFrame(columns=['tfidf']).from_dict(dict(tfidf), orient='index')
    tfidf = tfidf.reset_index()
    tfidf.columns = ['token','score']
    # normalize score
    tfidf['normalize_score']=(tfidf['score']-tfidf['score'].min())/(tfidf['score'].max()-tfidf['score'].min())
    return tfidf

def frequency_count_score(corpus):
    vectorizer = CountVectorizer()
    vz = vectorizer.fit_transform(corpus)
    freq_count = vectorizer.vocabulary_
    freq_count =pd.DataFrame(freq_count.items(),columns=['token','score'])
    #normalize score
    freq_count['normalize_score']=(freq_count['score']-freq_count['score'].min())/(freq_count['score'].max()-freq_count['score'].min())
    return freq_count

def get_confusion_matrics(actual,predict,labels):
    cm = confusion_matrix(actual, predict, labels=labels)
    cm = pd.DataFrame(cm,index=labels,columns=labels)
    return cm

def get_classification_report(actual,predict):
    cr = classification_report(actual, predict)
    return cr

def get_accuracy_score(actual,predict):
    return accuracy_score(actual, predict)