# Objective: scrape https://mudah.my to collect data and write to file
# script name: scrape_mudah.R
# script create date: 20/2/2019
# Required libraries: rvest, magritrr
library(rvest)
library(magrittr)
library(tidyverse)
library(stringr)

# clean the workspace
rm(list = ls())

# page url construction
base_url <- "https://www.mudah.my/Malaysia/for-sale?o=2&q=&md=li&th=0"
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

# Combine the data frames together.
# Apparently adPrice dataframe has more rows than adLoc dataframe, therefore to combine them we use the below technique
# Reference: https://stackoverflow.com/questions/14102498/merge-dataframes-different-lengths See answer of user G.Grothendieck

adLoc$x<- rownames(adLoc)
mudah.data = merge(adLoc, adPrice, by.x = 2, by.y = 0, all.x = TRUE)
# drop the x col
mudah.data$x <- NULL

## Export the data to csv
write.csv(mudah.data, file = "data/mudah_data.csv", row.names = FALSE)


##### Below code is test only

# extract the contents
siteHtml<- read_html(base_url)
adsPrice<- siteHtml %>%
  html_nodes(".ads_price") %>%
  html_text() %>%
  str_trim() %>%
  str_replace_all("[\r?\n\tper monthRM]","")%>%
  unlist()%>%
  as.integer()

# x <- setdiff(adLoc, adPrice)
# missing_data <-anti_join(adLoc, adPrice, by="adsPrice")


