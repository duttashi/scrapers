# This question was initially asked on SO: https://stackoverflow.com/questions/56186782/scrapping-400-pages-using-map

# clean the workspace
rm(list = ls())

# load the required libraries
library(rvest)
library(purrr)
library(tidyverse)
library(stringr)

# base url
blogurl<- "https://timesofindia.indiatimes.com/blogs/toi-editorials/page/1/"
# number of pages to scrape
pg_count <- 2
# browse to base url and get the html
#editorial_html <- read_html(blogurl)

# blog data
map_df(1:pg_count, function(i)
  {
  cat(".")
  pg <- read_html(sprintf(blogurl, i))
  data.frame(
    # Extract blog post date
    editorial_date = pg %>%
      html_nodes(xpath = "//span[@class='date']") %>%
      html_text()%>%
      str_trim() %>%
      unlist(),
    # Extract blog post time
    editorial_time = pg %>%
      html_nodes(xpath = "//span[@class='time']") %>%
      html_text()%>%
      str_trim() %>%
      unlist(),
    # Extract blog post headline
    editorial_headline = pg %>%
      html_nodes(xpath = "//h2[@class='media-heading']") %>%
      html_text()%>%
      str_trim() %>%
      str_to_lower(),
    # Extract blog post text
    editorial_text = pg %>%
      html_nodes(xpath = "//div[@class='content']//p") %>%
      html_text()%>%
      str_trim() %>%
      str_to_lower()
  )}
  )-> blog_data

# Add hyphens for spaces in editorial headline and store result in separate column
x<- gsub(":", "", blog_data$editorial_headline)
blog_data$editorial_headline_dashed<- gsub(" ", "-", x)

# browse to respective pages
fullposturl<- "https://timesofindia.indiatimes.com/blogs/toi-editorials/"
pg_count <- 2

map_df(1:pg_count, function(i)
{
  cat(".")
  pg <- read_html(sprintf(fullposturl,blog_data$editorial_headline_dashed[i]))
  data.frame(
    # Extract full blog post 
    blog_post_cmplt = pg %>%
      html_nodes(xpath = "div[@class='content']//p") %>%
      html_text()%>%
      str_trim() %>%
      str_to_lower()
  )}
)-> blog_data.x



# Pick value in editorial_headline_dashed THAN PASTE it to default url AND browse to the page TO EXTRACT the data
# editorial_html <- read_html(blogurl)
# 
# map_df(1:pg_count, function(i)
# {
#   cat(".")
#   pg <- read_html(sprintf(blogurl, i))
#   data.frame(
#     # Extract blog post date
#     editorial_text = pg %>%
#       html_nodes(xpath = "//div[@class='content']") %>%
#       html_text()%>%
#       str_trim() %>%
#       unlist()
#   )}
# )-> blog_data_text


