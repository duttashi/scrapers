#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Load the required libraries
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import pandas as pd
import json
import csv
import sys
import time


# In[3]:


# set the working environment including the keys for accessing twitter api
path="C:\\twitter_locations_n_scraper\\"


# Read the twitter credential file
creds_file="twitter_creds.txt"

with open(creds_file,'r') as f:
   
    mylist=[line.rstrip('\n') for line in f]

#print (mylist)


ckey = mylist[0] # The first element of the list
csecret = mylist[1] # The second element of the list
#print("ckey: "+consumer_key, "\ncs: "+consumer_secret)
atoken= mylist[2] # The third element of the list
asecret = mylist[3] # The last element of the list


# In[4]:


# create dataframe to store the results
def toDataFrame(tweets):
    # COnvert to data frame
    DataSet = pd.DataFrame()

    DataSet['tweetID'] = [tweet.id for tweet in tweets]
    DataSet['tweetText'] = [tweet.text.encode('utf-8') for tweet in tweets]
    DataSet['tweetRetweetCt'] = [tweet.retweet_count for tweet in tweets]
    DataSet['tweetFavoriteCt'] = [tweet.favorite_count for tweet in tweets]
    DataSet['tweetSource'] = [tweet.source for tweet in tweets]
    DataSet['tweetCreated'] = [tweet.created_at for tweet in tweets]
    DataSet['userID'] = [tweet.user.id for tweet in tweets]
    DataSet['userScreen'] = [tweet.user.screen_name for tweet in tweets]
    DataSet['userName'] = [tweet.user.name for tweet in tweets]
    DataSet['userCreateDt'] = [tweet.user.created_at for tweet in tweets]
    DataSet['userDesc'] = [tweet.user.description for tweet in tweets]
    DataSet['userFollowerCt'] = [tweet.user.followers_count for tweet in tweets]
    DataSet['userFriendsCt'] = [tweet.user.friends_count for tweet in tweets]
    DataSet['userLocation'] = [tweet.user.location for tweet in tweets]
    DataSet['userTimezone'] = [tweet.user.time_zone for tweet in tweets]
    DataSet['Coordinates'] = [tweet.coordinates for tweet in tweets]
    DataSet['GeoEnabled'] = [tweet.user.geo_enabled for tweet in tweets]
    DataSet['Language'] = [tweet.user.lang for tweet in tweets]
    tweets_place= []
    #users_retweeted = []
    for tweet in tweets:
        if tweet.place:
            tweets_place.append(tweet.place.full_name)
        else:
            tweets_place.append('null')
    DataSet['TweetPlace'] = [i for i in tweets_place]
    #DataSet['UserWhoRetweeted'] = [i for i in users_retweeted]

    return DataSet


# In[5]:


# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)


# In[6]:


# create the API
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)


# In[16]:


if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)
else:
    for tweet in tweepy.Cursor(api.search,q="rapidkl",
                               since='2018-05-01',until='2018-09-03',
                               lang='en',count=1000).items():
        print (tweet.created_at, tweet.text)


# In[ ]:




