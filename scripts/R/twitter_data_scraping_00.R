# Note: As per the documentation, you'll need to authenticate the twitter account api first. Once authentication is done, there is no need to do it each time you execute the program, unlike in python this is a must process.
## search for 18000 tweets using the rstats hashtag
# see this link for languages supported by twitter, https://developer.twitter.com/en/docs/twitter-for-websites/twitter-for-websites-supported-languages/overview.html
# create an external search string variable and then pass it to search_tweets()

# clean the workspace
rm(list = ls())

# required libraries
#library(rtweet)
library(tidytext)
library(tidyverse)
library(stringr)
library(stopwords)
library(rtweet) # for search_tweets()

# Create a function that will accept multiple hashtags and will search the twitter api for related tweets

search_tweets_queries <- function(x, n = 100, ...) {
  ## check inputs
  stopifnot(is.atomic(x), is.numeric(n))
  if (length(x) == 0L) {
    stop("No query found", call. = FALSE)
  }  
  ## search for each string in column of queries
  rt <- lapply(x, search_tweets, n = n, ...)
  ## add query variable to data frames
  rt <- Map(cbind, rt, query = x, stringsAsFactors = FALSE)
  ## merge users data into one data frame
  rt_users <- do.call("rbind", lapply(rt, users_data))
  ## merge tweets data into one data frame
  rt <- do.call("rbind", rt)
  ## set users attribute
  attr(rt, "users") <- rt_users
  ## return tibble (validate = FALSE makes it a bit faster)
  tibble::as_tibble(rt, validate = FALSE)
}

## create data frame with query column
df_query <- data.frame(
  query = c("KTM", "monorail","MRT"),
  #query = c("section377"),
  n = rnorm(3), # change this number according to the number of searchwords in parameter query. As of now, the parameter got 3 keywords, therefore this nuber is set to 3.
  stringsAsFactors = FALSE
)

# pass query column to the search_tweet_queries function defined above
df_collect_tweets <- search_tweets_queries(df_query$query, include_rts = FALSE,
                                        retryonratelimit = TRUE, 
                                        #geocode for Kuala Lumpur
                                        geocode = "3.14032,101.69466,93.5mi"
                                        # geocode for New Delhi
                                        #geocode="28.64386,77.12373,215mi"
                                        )

# Select and keep only relevant columns
df_select_tweets<- df_collect_tweets %>%
  select(c(user_id,created_at,screen_name, !is.na(hashtags),text,
           source,display_text_width>0,lang,!is.na(place_name),
           !is.na(place_full_name),
           !is.na(geo_coords), !is.na(country), !is.na(location),
           retweet_count,account_created_at, account_lang, query)
         )

# Saving the original extracted tweet data to a csv file
# First coerce the data.frame to all-character
df_orig_tweet_data<- data.frame(lapply(df_collect_tweets, as.character), stringsAsFactors = FALSE)
# write file
write.csv(df_orig_tweet_data,"C:\\Users\\Ashoo\\Documents\\Python Playground\\scrapers\\data\\tweets_orig_data.csv")

# Saving the selected columns data
df_select_tweets_1 = data.frame(lapply(df_select_tweets, as.character), stringsAsFactors=FALSE)
# write file
write.csv(df_select_tweets_1,"C:\\Users\\Ashoo\\Documents\\Python Playground\\scrapers\\data\\tweets_select_data.csv")

### Text preprocessing

# 1. Remove URL from text
# collapse to long format
clean_tweet<- df_select_tweets_1

#clean_tweet<- paste(df_select_tweets_1, collapse=" ")
clean_tweet$text = gsub("&amp", "", clean_tweet$text)
clean_tweet$text = gsub("(RT|via)((?:\\b\\W*@\\w+)+)", "", clean_tweet$text)
clean_tweet$text = gsub("@\\w+", "", clean_tweet$text)
clean_tweet$text = gsub("[[:punct:]]", "", clean_tweet$text)
clean_tweet$text = gsub("[[:digit:]]", "", clean_tweet$text)
clean_tweet$text = gsub("http\\w+", "", clean_tweet$text)
clean_tweet$text = gsub("[ \t]{2,}", "", clean_tweet$text)
clean_tweet$text = gsub("^\\s+|\\s+$", "", clean_tweet$text) 

#get rid of unnecessary spaces
clean_tweet$text <- str_replace_all(clean_tweet$text," "," ")
# Get rid of URLs
clean_tweet$text<- str_replace_all(clean_tweet$text, "https://t.co/[a-z,A-Z,0-9]*","")
clean_tweet$text<- str_replace_all(clean_tweet$text, "http://t.co/[a-z,A-Z,0-9]*","")
# Take out retweet header, there is only one
clean_tweet$text <- str_replace(clean_tweet$text,"RT @[a-z,A-Z]*: ","")
# Get rid of hashtags
clean_tweet$text <- str_replace_all(clean_tweet$text,"#[a-z,A-Z]*","")
# Get rid of references to other screennames
clean_tweet$text <- str_replace_all(clean_tweet$text,"@[a-z,A-Z]*","") 

# write to file
write.csv(clean_tweet,"C:\\Users\\Ashoo\\Documents\\Python Playground\\scrapers\\data\\tweets_select_data_clean.csv")


# 2. Unnest the tokens
df.clean<- clean_tweet %>%
  unnest_tokens(word, text)

clean_tweets<- tibble()
clean_tweets<- rbind(clean_tweets, df.clean)

# Basic calculations
# calculate word frequency
word_freq <- clean_tweets %>%
  count(word, sort=TRUE)
word_freq 

# lots of stop words like the, and, to, a etc. Let's remove the stop words. 
# We can remove the stop words from our tibble with anti_join and the built-in stop_words data set provided by tidytext.
# list all sources

# Reference
#stopwords::stopwords_getsources()
# list languages for a specific source
#stopwords::stopwords_getlanguages("stopwords-iso")

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
  ggtitle(paste('Most common words in tweets')) +
  theme(legend.position="none") +
  theme_minimal()+
  coord_flip()
