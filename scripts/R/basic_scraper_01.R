# script name: basic_scraper_01.R
# objective: To scrape http://www.ibilik.my/rooms/petaling_jaya for available rooms
# install selector gadget chrome extension for Google chrome
# use the selector gadget to find the relevant tag info
# press shift key on keyboard and unselect items not required on the webpage.
# see this website (https://selectorgadget.com/) to learn more about selector gadget
library(rvest)
library(magrittr)

siteLoc<- "http://www.ibilik.my/rooms/petaling_jaya"
siteLocHTML<- read_html(siteLoc)

room_location<-siteLocHTML %>%
  # using selector gadget to determine the css/xpath
  html_nodes(".lightblue a")%>%
  html_text()
head(room_location)
tail(room_location)

room_address <- siteLocHTML %>%
  html_nodes("p:nth-child(1)")%>%
  html_text()
head(room_address)

room_comment<-siteLocHTML %>%
  # using selector gadget to determine the css/xpath
  html_nodes("p")%>%
  html_text()
head(room_comment)

advert_post_date <- siteLocHTML %>%
  html_nodes(".lightblue+i") %>%
  html_text()
head(advert_post_date)




