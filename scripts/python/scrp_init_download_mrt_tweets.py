# install the library using pip3 install twint
# See the library at https://pypi.org/project/twint/

# Script create date: 02-Oct-2018
# Script Objective: To download data from twitter 

import twint

# Configure
c = twint.Config()
c.Store_csv = True
c.Custom = ["date","time", "id", "user_id", "username", "tweet","timezone","hashtags","location","replies","retweets","likes","link","user_rt","mentions"]
# Custom output format
c.Format = "Date: {date} | Time: {time}| Tweet id: {id}| User_ID: {userid}| UserName: {username}| Tweet: {tweet}"
# CSV Fieldnames
c.Output = "twitter_MRT_data.csv"
# Specifiy the search string
c.Search = "#MRT"
# Run the search
twint.run.Search(c)