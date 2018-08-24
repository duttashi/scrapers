# Objective: scraping news articles
# Script name: basic_scraper_02

# Load the libraries
library(XML)
library(RCurl)
library(stringr)

# news to scrape from
url<-"http://timesofindia.indiatimes.com/topic/Donald-Trump/news"

# Read the HTML of the web page
SOURCE<- getURL(url, encoding="UTF-8")
# Parse the HTML file and generate an R structure representing the XML/HTML tree
PARSED<- htmlParse(SOURCE)  

newsTitle <- xpathSApply(PARSED, "//*[contains(concat(' ',@class,' '), concat(' ', 'title', ' '))]",
                         xmlValue) 
# remove newline operator from title "\n"
newsTitle<- gsub("\\n","",newsTitle)
head(newsTitle)

newsPostTime<- xpathSApply(PARSED,"//*[contains(concat(' ', @class, ' '), concat(' ', 'meta', ' '))]",
                           xmlValue)
head(newsPostTime)

# Images to scrape
url<-"http://photogallery.indiatimes.com/fashion/foreign-models/pia-wurtzbach-and-iris-mittenaeres-photoshoot/articleshow/58591994.cms" 
SOURCE<- getURL(url, encoding="UTF-8")
PARSED<- htmlParse(SOURCE)
getImages<- xpathSApply(PARSED, "//*[contains(concat(' ',@class,' '), concat(' ', 'title', ' '))]",
                        xmlValue)