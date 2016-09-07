# Startup script to be run when server starts
# Generates a classifier and caches it
import classifiers

cache.ram('classifier', lambda: classifiers.get_twitter_classifier(), time_expire=60*60*24)

