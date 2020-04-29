# Objective: Scrape data from website www.eliteprospects.com
# I asked this question on SO https://stackoverflow.com/questions/52662005/how-to-scrape-data-from-multiple-pages-by-dynamically-updating-the-url-with-rves/56081334#56081334


library(rvest)
library(tidyverse)


scrape.draft = function(year){
  
  url = paste("https://www.eliteprospects.com/draft/nhl-entry-draft/",year,sep="")
  
  out = read_html(url) %>%
    html_table(header = T) %>% '[['(2) %>%
    filter(!grepl("ROUND",GP)) %>%
    mutate(draftYear = year)
  
  return(out)
  
}

temp = lapply(2010:2019,scrape.draft) %>%
  bind_rows()
temp
