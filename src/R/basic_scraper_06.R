
# RQ: Scrape the data from https://www.eliteprospects.com/
# The idea is user must provide the `draft name` and `year` as input. 
# The url will be constructed basis of this input. Then scrape the data
# The drafts are {NHL Entry Draft,NHL Expansion Draft,NHL Supplemental Draft,WHA Amateur Draft,KHL Draft,LNAH Draft,NWHL Draft,CWHL Draft   }
# More drafts can be found at the bottom of this page: https://www.eliteprospects.com/draft/nhl-entry-draft
# draft_year are Seasons for which the user wants to scrape data. Must be of the form 2018, 1996, etc -- only  a single 4-digit number.

# clean the workspace
rm(list = ls())

# load the required libraries
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

# For CSS, use the selector gadget from here: ftp://cran.r-project.org/pub/R/web/packages/rvest/vignettes/selectorgadget.html

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
  
  # Extract the seasons data
  draft_season<- page %>%
    # use selector gadget to determine the relevant css
    rvest::html_nodes(".seasons") %>%
    rvest::html_text()%>%
    stringr::str_squish() %>%
    tibble::as_tibble()
  
  # Extract the gp data
  draft_gp<- page %>%
    # use selector gadget to determine the relevant css
    rvest::html_nodes("#drafted-players .gp") %>%
    rvest::html_text()%>%
    stringr::str_squish() %>%
    tibble::as_tibble()
  
  # Extract the g data
  draft_g<- page %>%
    # use selector gadget to determine the relevant css
    rvest::html_nodes("#drafted-players .g") %>%
    rvest::html_text()%>%
    stringr::str_squish() %>%
    tibble::as_tibble()
  
  # Extract the a data
  draft_a<- page %>%
    # use selector gadget to determine the relevant css
    rvest::html_nodes("#drafted-players .a") %>%
    rvest::html_text()%>%
    stringr::str_squish() %>%
    tibble::as_tibble()
  
  # Extract the tp data
  draft_tp<- page %>%
    # use selector gadget to determine the relevant css
    rvest::html_nodes("#drafted-players .tp") %>%
    rvest::html_text()%>%
    stringr::str_squish() %>%
    tibble::as_tibble()
  
  # Extract the PIM data
  draft_pim<- page %>%
    # use selector gadget to determine the relevant css
    rvest::html_nodes(".pim") %>%
    rvest::html_text()%>%
    stringr::str_squish() %>%
    tibble::as_tibble()
  
  # Join the dataframe's together. 
  all_data<- cbind(draft_team, draft_player,draft_season, draft_gp,draft_g,
                   draft_a,draft_tp,draft_pim)  
  
  return(all_data)
  
} # end function


# Testing the function
draft_data<-get_draft_data("nhl entry draft", 2011)
View(draft_data)

draft_data<- get_draft_data("CWHL Draft","2012")
View(draft_data)

# Further improvement idea: Rather than user input, iterate through a list of draft teams and years to scrape the data.
# draft_year<- c(1963:2018)
# draft_year
draft_year<- c(2014:2018)
