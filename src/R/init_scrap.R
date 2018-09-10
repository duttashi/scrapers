library(rvest)
library(magrittr) # for the pipe operator
# RQ: Scrape the IMDB website for the most popular 100 movies of all times
# website to scrape
#site<- "http://www.propwall.my/"
#siteLoc<- "http://www.propwall.my/selangor"
siteLoc<- "http://www.ibilik.my/rooms/petaling_jaya"
# there are 20,835 titles for movies released between 2015-2016
siteLocHTML<- read_html(siteLoc)

# get the property listing comments

# Scrape the property location
siteLocHTML %>%
  html_nodes(".location")%>%
  html_text()
# Scrape the advertisement date
siteLocHTML %>%
  html_nodes(".date")%>%
  html_text()
# Scrape the advertisement date
siteLocHTML %>%
  html_nodes(".date")%>%
  html_text()

# Scrape the advertisement comments
siteLocHTML %>%
  html_nodes(".comment")%>%
  html_text()
# Scrape the advertisment views
siteLocHTML %>%
  html_nodes(".price_tag")%>%
  html_text()
# Scrape the advertisment title
siteLocHTML %>%
  html_nodes(xpath="//div[@class='title']//a")%>%
  html_text()
