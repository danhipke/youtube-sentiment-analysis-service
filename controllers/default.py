# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import nltk.classify.util
import classifier
import requests
import json

def extract_features(document):
    document_words = set(document)
    features = {}
    for document_word in document_words:
        features[document_word] = True
    #print features
    return features

def index():
    my_classifier = classifier.get_classifier()
    video_id = request.vars['videoId']
    url = 'https://www.googleapis.com/youtube/v3/commentThreads?part=id,snippet&videoId=' + video_id + '&order=relevance&key=AIzaSyB1NMklzwIEwson5THrPWB7eyfJ3o30Ydg'
    response = requests.get(url)
    sentiment_analysis_results = {}
    if (response.ok):
        jData = json.loads(response.content)
        items = jData['items']
        for item in items:
            comment_id = item['id']
            snippet = item['snippet']
            top_level_comment = snippet['topLevelComment']
            top_level_comment_snippet = top_level_comment['snippet']
            text_display = top_level_comment_snippet['textDisplay']
            sentiment_analysis_results[comment_id] = my_classifier.classify(extract_features(text_display.split()))


    else:
        print 'error contacting youtube api'


    #testfeats = classifier.get_testfeats()

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


