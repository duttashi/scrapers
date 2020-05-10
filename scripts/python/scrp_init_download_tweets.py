#!/usr/bin/env python
# coding: utf-8

# In[2]:


# download tweets older than a week
from .got3.manager import TweetCriteria
from .got3.manager import TweetManager
import sys
if sys.version_info[0] < 3:
    import got
else:
    import got3 as got


# In[ ]:


def main():
    # Example 2 - Get tweets by query search
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch('KTM').setSince("2018-01-01").setUntil("2018-06-30").setMaxTweets(1)
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
    printTweet("### Example 2 - Get tweets by query search [KTM]", tweet)
    
if __name__ == '__main__':
	main()

