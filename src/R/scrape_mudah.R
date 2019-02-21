# Objective: scrape https://mudah.my to collect data and write to file
# script name: scrape_mudah.R
# script create date: 20/2/2019

# clean the workspace
rm(list = ls())

# Required libraries: rvest, magritrr
library(rvest)
library(magrittr)
library(tidyverse)
library(stringr)

# page url construction
# base_url <- "https://www.mudah.my/Malaysia/for-sale?o=2&q=&md=li&th=0"
base_url <- "https://www.mudah.my/malaysia/for-sale"
#pg_count <- 31235
pg_count <- 20

# Extract the ad location data
map_df(1:pg_count, function(i)
{
  cat(".")
  pg <- read_html(sprintf(base_url, i))
  
  data.frame(
    adLoc = html_text(html_nodes(pg, ".area"))
    #,adPrice = html_text(html_nodes(pg, ".ads-price"))
    #adTitle = html_text( html_nodes(pg, "#list-views-ads a"))
    ,stringsAsFactors = FALSE
    )}
)-> adLoc

# Extract the ad price data
map_df(1:pg_count, function(i)
  {
  cat(".")
  pg <- read_html(sprintf(base_url, i))
  
  data.frame(
    adsPrice= pg %>%
    html_nodes(".ads_price") %>%
    html_text() %>%
    str_trim() %>%
    str_replace_all("[\r?\n\tper monthRM]","")%>%
    as.integer())
  }
  )-> adPrice

# Extract the ad title data
map_df(1:pg_count, function(i)
{
  cat(".")
  pg <- read_html(sprintf(base_url, i))
  
  data.frame(
    adsTitle= pg %>%
      html_nodes("h2 a") %>%
      html_text() %>%
      str_trim() %>%
      str_replace_all("[\r?\n\t?]","")%>%
      str_to_lower()
  )}
)-> adTitle

# Combine the data frames together.
# Apparently adPrice dataframe has more rows than adLoc dataframe, therefore to combine them we use the below technique
# Reference: https://stackoverflow.com/questions/14102498/merge-dataframes-different-lengths See answer of user G.Grothendieck

adLoc$x<- rownames(adLoc)
x.data = merge(adLoc, adPrice, by.x = 2, by.y = 0, all.x = TRUE)

adTitle$x<- rownames(adTitle)
mudah.data = merge(adTitle, x.data, by.x = 2, by.y = 0, all.x = TRUE)

# drop the x col
colnames(mudah.data)
mudah.data$x <- NULL
mudah.data$x.y<- NULL

## Export the data to csv
write.csv(mudah.data, file = "data/mudah_data.csv", row.names = FALSE)


##### Below code is test only

# extract the contents
siteHtml<- read_html(base_url)

adItem<- siteHtml %>%
  html_nodes(".house") %>%
  html_text()%>%
  str_trim() %>%
  str_replace_all("[\r?\n\t?]","")%>%
  str_to_lower()

adsPrice<- siteHtml %>%
  html_nodes(".ads_price") %>%
  html_text() %>%
  str_trim() %>%
  str_replace_all("[\r?\n\tper monthRM]","")%>%
  unlist()%>%
  as.integer()

adsTitle<- siteHtml %>%
  html_nodes(".list_title") %>%
  html_text()%>%
  str_trim() %>%
  str_replace_all("[\r?\n\t?]","")%>%
  str_to_lower()

adsCategory <- siteHtml %>%
  html_nodes(".vv") %>%
  html_text()%>%
  str_trim() %>%
  str_replace_all("[\r?\n\t?]","")%>%
  str_to_lower()

adsCondition<- siteHtml %>%
  html_nodes(".new-icon+ .icon_label")%>%
  html_text()%>%
  str_trim() %>%
  str_replace_all("[\r?\n\t?]","")%>%
  str_to_lower()%>%
  as.character()

adsPostDateTime<- siteHtml %>%
  html_nodes(".bottom_info div:nth-child(1)")%>%
  html_text()%>%
  str_trim() %>%
  str_replace_all("[\r?\n\t?]","")%>%
  str_to_lower()

head(adsPostDateTime, 10)
head(adDateTime, 10)
