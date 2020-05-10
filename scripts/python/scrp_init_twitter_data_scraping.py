#!/usr/bin/env python
# coding: utf-8

# Objective: Download data from twitter for hashtags #KTM, #MRT, #monorail using python library tweepy

# In[22]:


# import the required libraries
import tweepy
import csv


# In[23]:


# Open/Create a file to append data
csvFile = open('tweets.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)


# In[2]:


# Read the twitter credential file
creds_file="twitter_creds.txt"

with open(creds_file,'r') as f:
    mylist=[line.rstrip('\n') for line in f]

ckey = mylist[0] # The first element of the list
csecret = mylist[1] # The second element of the list
atoken= mylist[2] # The third element of the list
asecret = mylist[3] # The last element of the list


# In[3]:


# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


# In[32]:


for tweet in tweepy.Cursor(api.search,q="#MRT",count=100,
                       lang="en",rpp=100).items():
    print (tweet.created_at, tweet.futext)


# Now, let's improve the program a bit further. 
# 
# - Create a new variable called `searchString` and assign it a search word.
# - Create a `tweepy.Cursor` object such that it makes the code more readable and error-free.
# - Extract tweets within a certain time period, say tweets from Jan 1, 2018 until Sept 1, 2018.
# - Search for tweets in vernacular languages like, `bahasa melayu`, `hindi`, `indonesian` etc.
# - Include tweets greater than `140` characters. 

# In[83]:


# assign the search string
searchString = "#Malaysia"


# In[84]:


# creating the cursor object
# reference: http://docs.tweepy.org/en/latest/cursor_tutorial.html
# To print full text of the tweets, use `full_text`. See this github discussin answer by user LittleBigFrog https://github.com/tweepy/tweepy/issues/878

c = tweepy.Cursor(api.search, q=searchString, tweet_mode="extended", count=100,
                  lang="en", rpp=100,include_entities=True).items()


# In[28]:


# Avoid Rate limit exceeded error
while True:
    try:
        tweet = c.next()
        # Insert into db
        print (tweet.created_at, tweet.full_text, tweet.geo)
        # write data to a csv file
        csvWriter.writerow([tweet.created_at, tweet.full_text.encode('utf-8'), tweet.user.id])
        
    except tweepy.TweepError:
        # on rate limit exceeded, sleep for 5 minutes
        time.sleep(60 * 5)
        continue
    except StopIteration:
        break
    # close the csv file connection
    csvfile.close()


# ##### Now lets write a function to search for tweets within a specific geographic area, specifying coordinates and radius

# For trending hashtags in Malaysia, refer to this [website](https://trends24.in/malaysia/kuala-lumpur/)

# In[60]:


def searchWord(word, max_tweets, lang, geocode, since, out):
    # Query for 100 tweets that have word in them and store it in a list 
    searched_tweets = [status for status in tweepy.Cursor(api.search, n=max_tweets, q=word, lang=lang,  
                                                          geocode=geocode, since=since).items(max_tweets)]
    print("Number of Matches: %d\n" % len(searched_tweets))
    csvfile_my = open(out, 'w') # use `a` to append new data to old file. Use `w` to write new data to old file erasing the old data.
    csvWriter_my = csv.writer(csvfile_my)
    for t in searched_tweets:
        #print(t)
        csvWriter_my.writerow([t.created_at, t.text.encode('utf-8'), t.author.screen_name, t.place, t.retweeted, t.retweet_count, (not t.retweeted and 'RT @' not in t.text)])
        #print("\n Data written sucessfully")
    csvfile_my.close()


# In[78]:


# execute the method
searchWord('#Malaysia', 500, "en", "3.14032,101.69466,93.82mi", "2018-07-01",'malaysia_tweets.csv')


# ##### Note: Apparently, geo-coding does not allow to search for a specific keyword. See this [SO post](https://stackoverflow.com/questions/27319476/python-tweepy-find-all-tweets-in-the-netherlands). 
# If you want to extract tweets based on a specific keyword, then you'll have to remove the geo-code location. 

# In[80]:


def searchWord(word, max_tweets, lang, out):
    # Query for 100 tweets that have word in them and store it in a list 
    searched_tweets = [status for status in tweepy.Cursor(api.search, n=max_tweets, q=word, lang=lang).items(max_tweets)]
    print("Number of Matches: %d\n" % len(searched_tweets))
    csvfile_my = open(out, 'w') # use `a` to append new data to old file. Use `w` to write new data to old file erasing the old data.
    csvWriter_my = csv.writer(csvfile_my)
    for t in searched_tweets:
        #print(t)
        csvWriter_my.writerow([t.created_at, t.text.encode('utf-8'), t.author.screen_name, t.place, t.retweeted, t.retweet_count, (not t.retweeted and 'RT @' not in t.text)])
        #print("\n Data written sucessfully")
    csvfile_my.close()


# In[81]:


# execute the method
searchWord('#Malaysia', 500, "en", 'malaysia_tweets.csv')


# In[85]:


# Enough of printing the extracted tweets on the console, now let's save them to a list.
tweet_data=[]
import datetime

# set the start date
startDate = datetime.datetime(2018, 8, 31,0, 0, 0)
# set the end date
endDate =   datetime.datetime(2018, 8, 27,0, 0, 0)

# Avoid Rate limit exceeded error
while True:
    try:
        tweet = c.next()
        if tweet.created_at < endDate and tweet.created_at > startDate:
            #print the tweet on console
            print (tweet.created_at, tweet.full_text)
            # save the tweet to a list
            tweet_data.append(tweet)
        
        
    except tweepy.TweepError:
        # on rate limit exceeded, sleep for 5 minutes
        time.sleep(60 * 5)
        continue
    except StopIteration:
        break


# In[ ]:


See this SO post for the above error


# In[ ]:


# Extracting tweets within a certain date limit
# See this SO discussion https://stackoverflow.com/questions/49731259/tweepy-get-tweets-among-two-dates
# Apparently, twitter forbids this


# ##### Obtain tweets in bulk: Streaming with Tweepy
# See this [link](http://docs.tweepy.org/en/v3.6.0/streaming_how_to.html) for more information

# In[14]:


# load the required libraries
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


# #### Another example
# ##### Stop collecting tweets on reaching an `x` interval
# Reference: https://stackoverflow.com/questions/20863486/tweepy-streaming-stop-collecting-tweets-at-x-amount
