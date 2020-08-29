# Importing required libraries
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

# Generic Twitter class for sentiment analysis
class TwitterClient(object):
    def __init__(self):
        consumer_key = "svlrCWFSW6ph2x8KR3iTFY77N"
        consumer_secret = "Q9mzPGxjqxESbRpr3IZuc9AB8EcvoC97iUzZh27B3QtE4I1saR"
        access_token = "69556666-r4PibCcIi4KJlorLvTwC8QYuAmjQ9LaubWh35UF8K"
        access_token_secret = "RmgNvaoJ1wbCu1oVt1Tw6jGx9dyjHc7ou0BETkk6oRgww"

# Authentication
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)             # create OAuthHandler object
            self.auth.set_access_token(access_token, access_token_secret)       # set access tokens
            self.api = tweepy.API(self.auth)                                    # create tweepy API object to fetch tweets

        except:
            print("Error..Authentication failed !!")

 # Utility function to clean tweet text by removing links, special characters
    def clean_tweet(self, tweet):
        '''

        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\ / \ / \S+)", " ", tweet).split())

# Utility function to classify sentiment of passed tweet using textblob's sentiment method
    def get_tweet_sentiment(self,tweet):
        analysis = TextBlob(self.clean_tweet(tweet))                            # create TextBlob object of passed tweet text

        if analysis.sentiment.polarity > 0:                                     # set sentiment
            return "positive"
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

# Function to fetch tweets and parse them

    def get_tweets(self, query, count = 10):
        tweets = []
        try:

            fetched_tweets = self.api.search(q = query, count = count)              # call twitter api to fetch tweets

            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                if tweet.retweet_count > 0:

                    if parsed_tweet not in tweets:                                   # retweets are appended only once
                        tweets.append(parsed_tweet)
                else:
                        tweets.append(parsed_tweet)

            return tweets
        except tweepy.TweepError as e:                                              # print error if any
            print ("Error : " + str(e))

def main():
    api = TwitterClient()
    tweets = api.get_tweets("COVID19", count = 200)

    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']           # picking positive tweets
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))  # % of positive tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']           # picking negative tweets
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))  # % of negative tweets#
    print("Neutral tweets percentage: {} % \
          ".format(100 * (len(tweets) - (len(ntweets) + len(ptweets))) / len(tweets)))  # % of neutral tweets

    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
            print(tweet['text'])

if __name__ == "__main__":
    main()





