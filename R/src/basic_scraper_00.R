library(rvest)
library(magrittr) # for the pipe operator

# RQ: scrape my google scholar page for citations, year, corresponding author

siteLoc<- "https://scholar.google.com/citations?user=AIGfYdEAAAAJ&hl=en"
siteLocHTML<- read_html(siteLoc)

#get citations
citation_count<- siteLocHTML %>%
  # using selector gadget to determine the css/xpath
  html_nodes(".gsc_a_ac")%>%
  html_text()
head(citation_count)

cited_year<- siteLocHTML %>%
  html_nodes(".gsc_a_h") %>%
  html_text()
head(cited_year)

coauthor_and_journal<- siteLocHTML %>%
  html_nodes(".gs_gray") %>%
  html_text()
head(coauthor_and_journal)

