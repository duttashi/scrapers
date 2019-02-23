# Objective: scrape https://mudah.my to collect data and write to file
# script name: scrape_mudah.R
# script create date: 20/2/2019
# script last modified date: 23/2/2019

# clean the workspace
rm(list = ls())

# Required libraries: rvest, magritrr
library(rvest)
library(magrittr)
library(tidyverse)
library(stringr)
library(plyr)

# page url construction
# base_url <- "https://www.mudah.my/Malaysia/for-sale?o=2&q=&md=li&th=0"
base_url <- "https://www.mudah.my/malaysia/for-sale"
#pg_count <- 31235
pg_count <- 20

# Extract the ad data

# Note: the below function will not work because of unequal column length for one of the items
# error: error in data.frame : arguments imply differing number of rows: 40, 0
#reference: https://stackoverflow.com/questions/51706521/multiple-pages-in-rvest

map_df(1:pg_count, function(i)
{
  cat(".")
  pg <- read_html(sprintf(base_url, i))
  
  data.frame(
    itemArea = pg %>%
      html_nodes(".area") %>%
      html_text()%>%
      str_trim() %>%
      unlist()
    ,stringsAsFactors = TRUE
  )}
)-> advert.area

# Price
map_df(1:pg_count, function(i)
{
  cat(".")
  pg <- read_html(sprintf(base_url, i))
  
  data.frame(
    itemPrice = pg %>%
      html_nodes(".ads_price") %>%
      html_text()%>%
      str_trim() %>%
      str_replace_all("[\r?\n\tper monthRM]","")%>%
      unlist()%>%
      as.integer()
    ,stringsAsFactors = TRUE
  )}
)-> advert.price


# Advert Title
map_df(1:pg_count, function(i)
{
  cat(".")
  pg <- read_html(sprintf(base_url, i))
  
  data.frame(
    itemTitle= pg %>%
      html_nodes("h2 a") %>%
      html_text() %>%
      str_trim() %>%
      str_replace_all("[\r?\n\t?]","")%>%
      str_to_lower()
  )}
)-> advert.title

# Advert Category
map_df(1:pg_count, function(i)
{
  cat(".")
  pg <- read_html(sprintf(base_url, i))
  
  data.frame(
    itemCat = pg %>%
      html_nodes(".vv") %>%
      html_text()%>%
      str_trim() %>%
      unlist()
    ,stringsAsFactors = TRUE
  )}
)-> advert.catgry

# Advert Condition
map_df(1:pg_count, function(i)
{
  cat(".")
  pg <- read_html(sprintf(base_url, i))
  
  data.frame(
    itemCondt = pg %>%
      html_nodes(".new-icon+ .icon_label") %>%
      html_text()%>%
      str_trim() %>%
      unlist()
    ,stringsAsFactors = TRUE
  )}
)-> advert.condt

# Advert post date time
map_df(1:pg_count, function(i)
{
  cat(".")
  
  pg <- read_html(sprintf(base_url, i))
  
  data.frame(
    itemDateTime = pg %>%
      html_nodes(".bottom_info div:nth-child(1)")%>%
      html_text()%>%
      str_trim() %>%
      str_replace_all("[\r?\n\t?]","")%>%
      str_to_lower()
    ,stringsAsFactors = TRUE
  ) }
)-> advert.datetime



# Combine the data frames together.
# Apparently adPrice dataframe has more rows than adLoc dataframe, therefore to combine them we use the below technique
# Reference: https://stackoverflow.com/questions/14102498/merge-dataframes-different-lengths See answer of user G.Grothendieck

#merge(A, B, by = 0, all = TRUE)[-1] .

# merge title & price
a<- merge(advert.title, advert.price,by = 0, all = TRUE)[-1]
colnames(a)
# merge (title, price) with datetime
b<- merge(a, advert.datetime,by = 0, all = TRUE)[-1]
colnames(b)

# merge category & condition
c <- merge(advert.catgry, advert.condt,by = 0, all = TRUE)[-1]
colnames(c)
# merge (title, price, datetime) & (category, condition)
d <- merge(b, c,by = 0, all = TRUE)[-1]
colnames(d)
# merge (title, price, datetime,category, condition) & area
e <- merge(d, advert.area,by = 0, all = TRUE)[-1]
colnames(e)
df.final<- e

head(df.final)

## Export the data to csv
write.csv(df.final, file = "data/mudah_data.csv", row.names = FALSE)


# ##### Below code is test only
# 
# # extract the contents
# siteHtml<- read_html(base_url)
# 
# adItem<- siteHtml %>%
#   html_nodes(".house") %>%
#   html_text()%>%
#   str_trim() %>%
#   str_replace_all("[\r?\n\t?]","")%>%
#   str_to_lower()
# 
# adsPrice<- siteHtml %>%
#   html_nodes(".ads_price") %>%
#   html_text() %>%
#   str_trim() %>%
#   str_replace_all("[\r?\n\tper monthRM]","")%>%
#   unlist()%>%
#   as.integer()
# 
# adsTitle<- siteHtml %>%
#   html_nodes(".list_title") %>%
#   html_text()%>%
#   str_trim() %>%
#   str_replace_all("[\r?\n\t?]","")%>%
#   str_to_lower()
# 
# adsCategory <- siteHtml %>%
#   html_nodes(".vv") %>%
#   html_text()%>%
#   str_trim() %>%
#   str_replace_all("[\r?\n\t?]","")%>%
#   str_to_lower()
# 
# adsCondition<- siteHtml %>%
#   html_nodes(".new-icon+ .icon_label")%>%
#   html_text()%>%
#   str_trim() %>%
#   str_replace_all("[\r?\n\t?]","")%>%
#   str_to_lower()%>%
#   as.character()
# 
# adsPostDateTime<- siteHtml %>%
#   html_nodes(".bottom_info div:nth-child(1)")%>%
#   html_text()%>%
#   str_trim() %>%
#   str_replace_all("[\r?\n\t?]","")%>%
#   str_to_lower()
# 
# head(adsPostDateTime, 10)
# head(adDateTime, 10)
