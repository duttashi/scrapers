# Web scraping with rvest package
# script name: basic_scraper_03.R

library(rvest)
library(magrittr)
urlPage<- read_html("http://timesofindia.indiatimes.com/india", encoding = 'UTF-8')
guess_encoding(urlPage)

urlPage %>%
  html_nodes("li span") %>%
  html_text()