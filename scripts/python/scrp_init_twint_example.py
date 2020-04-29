import twint
# Configure
# c = twint.Config()
# c1 = twint.Config()
c2= twint.Config()

# CSV Fieldnames
# c.Store_csv = True
# c.Custom = ["date","time", "id", "user_id", "username", "tweet","timezone","hashtags","location","replies","retweets","likes","link","user_rt","mentions"]
# # Custom output format
# c.Format = "Date: {date} | Time: {time}| Tweet id: {id}| User_ID: {userid}| UserName: {username}| Tweet: {tweet}"
# c.Output = "twitter_KTM_data.csv"
# c.Search = "#KTM"
# twint.run.Search(c)

# CSV Fieldnames
# c1.Store_csv = True
# c1.Custom = ["date","time", "id", "user_id", "username", "tweet","timezone","hashtags","location","replies","retweets","likes","link","user_rt","mentions"]
# c1.Format = "Date: {date} | Time: {time}| Tweet id: {id}| User_ID: {userid}| UserName: {username}| Tweet: {tweet}"
# c1.Since = "2015-01-01"
# c1.Until = "2018-10-02"
# # c1.Fruit = True
# # c1.Limit = 20
# c1.Output = "twitter_monorail_data.csv"
# c1.Search = "#monorail"
# twint.run.Search(c1)


# # CSV Fieldnames
c2.Store_csv = True
c2.Custom = ["date","time", "id", "user_id", "username", "tweet","timezone","hashtags","location","replies","retweets","likes","link","user_rt","mentions"]
c2.Since = "2015-01-01"
c2.Until = "2018-10-02"
c2.Output = "twitter_MRT_data.csv"
c2.Search = "#MRT"
twint.run.Search(c2)