# YouTube Sentiment Analysis Service

This is a web2py application that analyzes YouTube comment sentiment and classifies each comment as positive ('pos') or negative ('neg').

## Setup
Currently, the classifier is trained on a the publicly available Twitter Sentiment Analysis Dataset (http://thinknook.com/wp-content/uploads/2012/09/Sentiment-Analysis-Dataset.zip). To train the classifier you need to download the dataset, unzip it and copy the CSV to your web2py installation folder under **data/twitter-sentiment-analysis-dataset.csv** (at the same level as the **applications** folder). This is where the classifier loads data from.

Next, under the **youtube_sentiment_analysis_service** application, you need to copy **modules/youtubedataapi_settings_sample.py** to **modules/youtubedataapi_settings.py** and fill in youtubedataapi_key. Information on getting an API key is here https://developers.google.com/youtube/v3/getting-started

Now you can startup Web2Py and go to the following URL (hostname/port may vary depending on where it is run):

http://localhost:8000/youtube_sentiment_analysis_service/default/index.json?videoId=_GuOjXYl5ew

Hitting this URL does two things:
* trains the classifier and pickles it
* analyzes the sentiment of a specific video with ID **_GuOjXYl5ew**

Training the classifier takes about 10 minutes. The service trains the classifier if it can't find a pickled one on disk. After the first train, the classifier is pickled.

## Next Steps
The next step is building out functionality to allow creation of a sentiment analysis dataset specifically for YouTube comments. Although Twitter sentiment serves as an okay proxy for YouTube comment sentiment, specific data for this domain is preferable.
