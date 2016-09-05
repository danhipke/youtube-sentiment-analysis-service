# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import nltk.classify.util
import json
import csv
import os
import cPickle as pickle
from nltk import NaiveBayesClassifier, word_tokenize
from youtubedataapi_w import YouTubeDataAPI


def word_feats(words):
    my_word_feats = dict([(word, True) for word in words])
    return my_word_feats


def get_classifier():
    classifier = cache.ram('classifier', lambda: get_classifier_from_disk(), time_expire=60*60*24)
    return classifier


def get_classifier_from_disk():
    if os.path.isfile('my_classifier.pickle'):
        print 'Loading classifier from pickle'
        classifier = pickle.load(open('my_classifier.pickle', 'rb'))
    else:
        print 'Training classifier'

        negfeats = []
        posfeats = []

        with open(os.path.join(request.folder, 'data', 'twitter-sentiment-analysis-dataset.csv')) as csvfile:
            tweet_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            #skip first line
            tweet_reader.next()
            count = 0;
            for tweet in tweet_reader:
                words = word_tokenize(unicode(tweet[3].lower(), 'utf-8'))
                if tweet[1] == '1':
                    posfeats.append((word_feats(words), 'pos'))
                else:
                    negfeats.append((word_feats(words), 'neg'))
                count += 1

        negcutoff = len(negfeats) * 9 / 10
        poscutoff = len(posfeats) * 9 / 10

        trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
        testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
        print 'Training on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))

        classifier = NaiveBayesClassifier.train(trainfeats)
        pickle.dump(classifier, open('my_classifier.pickle', 'wb'))
        print 'Accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
        classifier.show_most_informative_features()
    return classifier

def extract_features(document):
    document_words = set(document)
    features = {}
    for document_word in document_words:
        features[document_word] = True
    return features


def index():
    my_classifier = get_classifier()
    video_id = request.vars['videoId']
    youtube = YouTubeDataAPI()
    response = youtube.get_comment_threads(videoId=video_id)
    sentiment_analysis_results = {}
    jData = json.loads(response)
    items = jData['items']

    for item in items:
        comment_id = item['id']
        snippet = item['snippet']
        top_level_comment = snippet['topLevelComment']
        top_level_comment_snippet = top_level_comment['snippet']
        text_display = top_level_comment_snippet['textDisplay']
        sentiment_analysis_results[comment_id] = my_classifier.classify(extract_features(text_display.split()))

    return dict(results=sentiment_analysis_results)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


