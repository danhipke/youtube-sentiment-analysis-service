import nltk.classify.util
import csv
import os
import cPickle as pickle
from nltk import NaiveBayesClassifier
from nltk.corpus import movie_reviews

def word_feats(words):
    return dict([(word, True) for word in words])

def get_classifier():
    if os.path.isfile('my_classifier.pickle'):
        classifier = pickle.load(open('my_classifier.pickle', 'rb'))
    else:
        negids = movie_reviews.fileids('neg')
        posids = movie_reviews.fileids('pos')

        #negfeats = []
        #posfeats = []

        negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
        posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]


        #with open('data/twitter-sentiment-analysis-dataset.csv', 'rb') as csvfile:
        #    tweet_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        #    for tweet in tweet_reader:
        #        if tweet[1] == '1':
        #            print "positive tweet"
        #        else:
        #            print "negative tweet"

        negcutoff = len(negfeats) * 3 / 4
        poscutoff = len(posfeats) * 3 / 4

        trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
        testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
        print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))

        classifier = NaiveBayesClassifier.train(trainfeats)
        pickle.dump(classifier, open('my_classifier.pickle', 'wb'))
        pickle.dump(testfeats, open('testfeats.pickle', 'wb'))
        print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
        classifier.show_most_informative_features()
    return classifier

def get_testfeats():
    return pickle.load(open('testfeats.pickle', 'rb'))