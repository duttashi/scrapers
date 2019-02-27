# Objective: scrape https://mudah.my to collect data and write to file
# script name: scrape_mudah.R
# script create date: 20/2/2019
# script last modified date: 23/2/2019

# clean the workspace
rm(list = ls())

# Required libraries: rvest, magritrr
library(rvest)
library(plyr)
library(magrittr)
library(tidyverse)
library(stringr)


# page url construction
base_url <- "https://www.mudah.my/malaysia/for-sale"
#pg_count <- 31235
pg_count <- 500

# Extract the ad data
#reference: https://stackoverflow.com/questions/51706521/multiple-pages-in-rvest
# Note: The variables, "Price, Title, DateTime" have common number of rows (n=820), so I've put them into a single function.
# The remaining variables have different number of rows, therefore they are put in separate functions which are later merged together

# Price, Title, DateTime 
map_df(1:pg_count, function(i)
{
  cat(".")
  pg <- read_html(sprintf(base_url, i))
  
  data.frame(
    # Extract Item Price
    itemPrice = pg %>%
      html_nodes(".ads_price") %>%
      html_text()%>%
      str_trim() %>%
      str_replace_all("[\r?\n\tper monthRM]","")%>%
      unlist()%>%
      as.integer(),
    # Extract Item Title
    itemTitle= pg %>%
      html_nodes("h2 a") %>%
      html_text() %>%
      str_trim() %>%
      str_replace_all("[\r?\n\t?]","")%>%
      str_to_lower(),
    # Extract Item date time
    itemDateTime = pg %>%
      html_nodes(".bottom_info div:nth-child(1)")%>%
      html_text()%>%
      str_trim() %>%
      str_replace_all("[\r?\n\t?]","")%>%
      str_to_lower()
    ,stringsAsFactors = TRUE
  )}
)-> advert.PriceTitleDate

# Advert Area
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
    ,stringsAsFactors = FALSE
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
    ,stringsAsFactors = FALSE
  )}
)-> advert.condt

# Combine the data frames together.
# Apparently adPrice dataframe has more rows than adLoc dataframe, therefore to combine them we use the below technique
# Reference: https://stackoverflow.com/questions/14102498/merge-dataframes-different-lengths See answer of user G.Grothendieck

# merge category & condition
a <- merge(advert.catgry, advert.condt,by = 0, all = TRUE)[-1]
colSums(is.na(a))
# merge (category, condition with area)
b<- merge(a, advert.area,by = 0, all = TRUE)[-1]
colSums(is.na(b))
# merge (category, condition, area) with (title, price, datetime)
c<- merge(advert.PriceTitleDate, b,by = 0, all = TRUE)[-1]
colnames(c)
# make a copy
df.final<- c

# Look at the data
dim(df.final)
head(df.final)
tail(df.final)
# missing values
colSums(is.na(df.final))

# rearrange the columns
colnames(df.final)
df.final<- df.final[, c(3,2,6,4:5,1)]
colnames(df.final)
head(df.final)
## Export the data to csv
write.csv(df.final, file = "data/mudah_data.csv", row.names = FALSE)
