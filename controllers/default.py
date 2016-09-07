# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import json

from applications.youtube_sentiment_analysis_service.modules import classifiers
from youtubedataapi_w import YouTubeDataAPI

def extract_features(document):
    document_words = set(document)
    features = {}
    for document_word in document_words:
        features[document_word] = True
    return features

def get_classifier():
    classifier = cache.ram('classifier', lambda: classifiers.get_twitter_classifier(), time_expire=60*60*24)
    return classifier


def index():
    my_classifier = get_classifier()
    video_id = request.vars['videoId']
    page_token = request.vars['pageToken']
    if not page_token:
        page_token = ''
    youtube = YouTubeDataAPI()
    response = youtube.get_comment_threads(videoId=video_id, pageToken=page_token)
    sentiment_analysis_results = {}
    jData = json.loads(response)
    #print jData
    next_page_token = jData['nextPageToken']
    items = jData['items']

    for item in items:
        comment_id = item['id']
        snippet = item['snippet']
        top_level_comment = snippet['topLevelComment']
        top_level_comment_snippet = top_level_comment['snippet']
        text_display = top_level_comment_snippet['textDisplay']
        sentiment_analysis_results[comment_id] = my_classifier.classify(extract_features(text_display.split()))

    return dict(results=sentiment_analysis_results, nextPageToken=next_page_token)


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


