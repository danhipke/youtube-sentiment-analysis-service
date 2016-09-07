import csv
import os

import nltk
import cPickle as pickle
from nltk import NaiveBayesClassifier
from nltk.corpus import movie_reviews


def get_twitter_classifier():
    if os.path.isfile('twitter_classifier.pickle'):
        print 'Loading twitter classifier from pickle...'
        classifier = pickle.load(open('twitter_classifier.pickle', 'rb'))
    else:
        print 'Generating new twitter classifier...'
        classifier = generate_twitter_classifier(os.path.join('data', 'twitter-sentiment-analysis-dataset.csv'))
        print 'Saving twitter classifier...'
        pickle.dump(classifier, open("twitter_classifier.pickle", "wb"))
    return classifier


def _word_feats(words):
    my_word_feats = dict([(word, True) for word in words])
    return my_word_feats


def generate_twitter_classifier(twitter_dataset_input_filename):
    neg_feats = []
    pos_feats = []

    with open(twitter_dataset_input_filename) as csvfile:
        tweet_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # skip header line
        tweet_reader.next()
        count = 0;
        for tweet in tweet_reader:
            words = nltk.word_tokenize(unicode(tweet[3].lower(), 'utf-8'))
            if tweet[1] == '1':
                pos_feats.append((_word_feats(words), 'pos'))
            else:
                neg_feats.append((_word_feats(words), 'neg'))
            count += 1

    return _train_and_test_bayes_classifier(neg_feats, pos_feats)


def generate_movie_review_classifier():
    neg_ids = movie_reviews.fileids('neg')
    pos_ids = movie_reviews.fileids('pos')

    neg_feats = [(_word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in neg_ids]
    pos_feats = [(_word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in pos_ids]

    return _train_and_test_bayes_classifier(neg_feats, pos_feats)


def _train_and_test_bayes_classifier(neg_feats, pos_feats):
    #TODO: Make this fraction configurable
    neg_cutoff = len(neg_feats) * 9 / 10
    pos_cutoff = len(pos_feats) * 9 / 10

    train_feats = neg_feats[:neg_cutoff] + pos_feats[:pos_cutoff]
    test_feats = neg_feats[neg_cutoff:] + pos_feats[pos_cutoff:]

    print 'Train on %d instances, Test on %d instances' % (len(train_feats), len(test_feats))

    classifier = NaiveBayesClassifier.train(train_feats)

    print 'Accuracy:', nltk.classify.util.accuracy(classifier, test_feats)
    return classifier
