
# RQ: Scrape the data from https://www.eliteprospects.com/
# The idea is user must provide the `draft name` and `year` as input. 
# The url will be constructed basis of this input. Then scrape the data
# The drafts are {NHL Entry Draft,NHL Expansion Draft,NHL Supplemental Draft,WHA Amateur Draft,KHL Draft,LNAH Draft,NWHL Draft,CWHL Draft   }
# More drafts can be found at the bottom of this page: https://www.eliteprospects.com/draft/nhl-entry-draft
# draft_year are Seasons for which the user wants to scrape data. Must be of the form 2018, 1996, etc -- only  a single 4-digit number.


library(rvest)

# LOGIC: First create test example to check if the idea works. Then put it all in a function

# manual assignment
# draft_type<- "nhl entry draft"
# draft_types<- draft_type %>%
#   # coerce to tibble format
#   tibble::as.tibble() %>%
#   purrr::set_names("draft_type") %>% 
#   # replace the space between words in draft type with a '-'. 
#   # The space is replaced with hyphen because if you browse to the webpage, you'll see the page is constructed the same. https://www.eliteprospects.com/draft/nhl-entry-draft
#   dplyr::mutate(draft_type = stringr::str_replace_all(draft_type, " ", "-"))
# 
# draft_year<- 2018
# # create page url
# page <- stringr::str_c("https://www.eliteprospects.com/draft/", draft_types, "/", draft_year)%>%
#   xml2::read_html()
# # Now scrape the team data from the page
# # Extract the team data
# draft_team<- page %>%
#   # use selector gadget to determine the relevant css
#   rvest::html_nodes(".team") %>%
#   rvest::html_text()%>%
#   stringr::str_squish() %>%
#   tibble::as_tibble()
# 
# # Extract the player data
# draft_player<- page %>%
#   # use selector gadget to determine the relevant css
#   rvest::html_nodes("#drafted-players .player") %>%
#   rvest::html_text()%>%
#   stringr::str_squish() %>%
#   tibble::as_tibble()
# 
# # Join both the dataframe's together. Note both dataframes have uneven rows. So using merge
# all_data<- cbind(draft_team, draft_player)

# The above logic works. Wraping it in a function

get_draft_data<- function(draft_type, draft_year){
  
  # replace the space between words in draft type with a '-'
  draft_types<- draft_type %>%
    # coerce to tibble format
    tibble::as.tibble() %>%
    purrr::set_names("draft_type") %>% 
    # replace the space between words in draft type with a '-'
    dplyr::mutate(draft_type = stringr::str_replace_all(draft_type, " ", "-"))
  
  # create page url
  page <- stringr::str_c("https://www.eliteprospects.com/draft/", draft_types, "/", draft_year)%>%
    xml2::read_html()
  
  # Now scrape the team data from the page
  # Extract the team data
  draft_team<- page %>%
    # use selector gadget to determine the relevant css
    rvest::html_nodes(".team") %>%
    rvest::html_text()%>%
    stringr::str_squish() %>%
    tibble::as_tibble()
  
  # Extract the player data
  draft_player<- page %>%
    # use selector gadget to determine the relevant css
    rvest::html_nodes("#drafted-players .player") %>%
    rvest::html_text()%>%
    stringr::str_squish() %>%
    tibble::as_tibble()
  
  # Join both the dataframe's together. Note both dataframes have uneven rows. So using merge
  all_data<- cbind(draft_team, draft_player)  
  
  return(all_data)
  
} # end function


# Testing the function
draft_data<-get_draft_data("nhl entry draft", 2018)
draft_data

draft_data<- get_draft_data("CWHL Draft","2018")
View(draft_data)

# Further improvement idea: Rather than user input, iterate through a list of draft teams and years to scrape the data.






