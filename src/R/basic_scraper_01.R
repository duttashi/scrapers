# script name: basic_scraper_01.R
# objective: To scrape http://www.ibilik.my/rooms/petaling_jaya for available rooms

library(rvest)
library(magrittr)

siteLoc<- "http://www.ibilik.my/rooms/petaling_jaya"
siteLocHTML<- read_html(siteLoc)

room_location<-siteLocHTML %>%
  # using selector gadget to determine the css/xpath
  html_nodes(".location")%>%
  html_text()
head(room_location)
tail(room_location)

room_comment<-siteLocHTML %>%
  # using selector gadget to determine the css/xpath
  html_nodes(".comment")%>%
  html_text()
head(room_comment)


