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

# get the total number of pages
tot_page_count <- siteLocHTML %>%
  # using selector gadget to determine the css/xpath
  html_nodes(".brightblue+ .brightblue")%>%
  html_text() %>%
  as.numeric()
tot_page_count


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
  html_nodes("p:nth-child(1)")%>%
  html_text()
head(room_comment)

advert_post_date <- siteLocHTML %>%
  html_nodes(".lightblue+i") %>%
  html_text()
head(advert_post_date)

room_conditions <- siteLocHTML %>%
  html_nodes("p:nth-child(2)")%>%
  html_text()
head(room_conditions)  

room_size <- siteLocHTML %>%
  html_nodes("p:nth-child(3)")%>%
  html_text()
head(room_size)

room_facility <- siteLocHTML %>%
  html_nodes("p:nth-child(4)")%>%
  html_text()
head(room_facility)

advert_view_count <- siteLocHTML %>%
  html_nodes(".home-list-pop-rat")%>%
  html_text()
head(advert_view_count)

room_rent <- siteLocHTML %>%
  html_nodes(".room_price span")%>%
  html_text()
head(room_rent)

