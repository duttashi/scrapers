# Objective: Data analysis of tweets based on hashtag #MRT
# Data collection time frame: 01-01-2015 until 02-10-2018
# Data collection script: Python 3.6
# Data collection libraries: twint  


# clean the environment
rm(list = ls())

# required libraries
#library(rtweet)
library(tidytext)
library(tidyverse)
library(stringr)
library(stopwords)

# Load the data
dat<- read.csv("~/Python Playground/scrapers/data/twitter_MRT_data.csv", header = TRUE, sep = ",")

# EDA
View(dat)
names(dat) # view the column names

# Select and keep only relevant columns
df_select_tweets<- dat %>%
  select(c(date,username,tweet,!is.na(hashtags) ,!is.na(location) )
  )

# Coerce the data.frame to all-character
df_select_tweets = data.frame(lapply(df_select_tweets, as.character), stringsAsFactors=FALSE)

# Text preprocessing

# create a copy of the df
clean_tweet<- df_select_tweets

clean_tweet$tweet = gsub("&amp", "",clean_tweet$tweet)
clean_tweet$tweet = gsub("&amp", "", clean_tweet$tweet)
clean_tweet$tweet = gsub("(RT|via)((?:\\b\\W*@\\w+)+)", "", clean_tweet$tweet)
clean_tweet$tweet = gsub("@\\w+", "", clean_tweet$tweet)
clean_tweet$tweet = gsub("[[:punct:]]", "", clean_tweet$tweet)
clean_tweet$tweet = gsub("[[:digit:]]", "", clean_tweet$tweet)
clean_tweet$tweet = gsub("http\\w+", "", clean_tweet$tweet)
clean_tweet$tweet = gsub("[ \t]{2,}", "", clean_tweet$tweet)
clean_tweet$tweet = gsub("^\\s+|\\s+$", "", clean_tweet$tweet) 
clean_tweet$tweet = gsub('[^\x20-\x7E]', '', clean_tweet$tweet) # for removing strange characters. See this SO thread https://stackoverflow.com/questions/38828620/how-to-remove-strange-characters-using-gsub-in-r
#get rid of unnecessary spaces
clean_tweet$tweet <- str_replace_all(clean_tweet$tweet," "," ")
# Get rid of URLs
clean_tweet$tweet<- str_replace_all(clean_tweet$tweet, "https://t.co/[a-z,A-Z,0-9]*","")
clean_tweet$tweet<- str_replace_all(clean_tweet$tweet, "http://t.co/[a-z,A-Z,0-9]*","")
# Take out retweet header, there is only one
clean_tweet$tweet <- str_replace(clean_tweet$tweet,"RT @[a-z,A-Z]*: ","")
# Get rid of hashtags
clean_tweet$tweet <- str_replace_all(clean_tweet$tweet,"#[a-z,A-Z]*","")
# Get rid of references to other screennames
clean_tweet$tweet <- str_replace_all(clean_tweet$tweet,"@[a-z,A-Z]*","") 

# write to file
write.csv(clean_tweet,"~/Python Playground/scrapers/data/twitter_MRT_data_clean.csv")


# 2. Unnest the tokens
df.clean<- clean_tweet %>%
  unnest_tokens(word, tweet)


# Basic calculations
# calculate word frequency
word_freq <- clean_tweets %>%
  count(word, sort=TRUE)
head(word_freq,10) 

# lots of stop words like the, and, to, a etc. Let's remove the stop words. 
# We can remove the stop words from our tibble with anti_join and the built-in stop_words data set provided by tidytext.
# use stopwords-iso list 
clean_tweets %>%
  # remove the stopwords in Bahasa Melayu (BM). Use `ms` for BM. See this reference for other language codes: https://en.wikipedia.org/wiki/ISO_639-1
  anti_join(get_stopwords(language="ms", source="stopwords-iso")) %>%
  # remove the stopwords in english
  anti_join(get_stopwords(language="en", source="stopwords-iso")) %>%
  count(word, sort=TRUE) %>%
  top_n(10) %>%
  ggplot(aes(word,n, fill=word))+
  geom_bar(stat = "identity")+
  xlab(NULL)+
  ylab(paste('Word count'))+
  ggtitle(paste('Common words in #MRT tweets from Jan 2015 until Oct 2018')) +
  theme(legend.position="none") +
  theme_minimal()+
  coord_flip()
