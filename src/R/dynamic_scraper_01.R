# Objective: Scarping dynamic webpages using rvest & RSelenium
# script name: dynamic_scraper_01

library(rvest)
library(RSelenium)
library(stringr)

# url to scrape
url<-"http://timesofindia.indiatimes.com/"
search <- "trump"
url <- paste(url,"search?q=",search,sep = "")

