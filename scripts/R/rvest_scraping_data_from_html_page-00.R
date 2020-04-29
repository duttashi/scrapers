# This question was originally asked on SO
# question: https://stackoverflow.com/questions/56068532/r-scraping-data-after-post-only-works-for-first-page/56069395#56069395


library(rvest)
library(dplyr)


url <- "http://www.spezialitaetenliste.ch/ShowPreparations.aspx?searchType=Substance&searchValue="
pgsession<-html_session(url)
pgform<-html_form(pgsession)[[1]]

page<-rvest:::request_POST(pgsession,url,
                           body=list(
                             `ctl00$cphContent$gvwPreparations$ctl13$gvwpPreparations$txtPageNumber`=3,
                             `__VIEWSTATE`=pgform$fields$`__VIEWSTATE`$value,
                             `__VIEWSTATEGENERATOR`=pgform$fields$`__VIEWSTATEGENERATOR`$value,
                             `__VIEWSTATEENCRYPTED`=pgform$fields$`__VIEWSTATEENCRYPTED`$value,
                             `__EVENTVALIDATION`=pgform$fields$`__EVENTVALIDATION`$value,
                             `ctl00$cphContent$gvwPreparations$ctl13$gvwpPreparations$ddlPageSize`="10",
                             `__EVENTTARGET`="ctl00$cphContent$gvwPreparations$ctl02$ctl00",
                             `__EVENTARGUMENT`=""
                             
                           ),
                           encode="form")
# makes a table of all results of the first page

read_html(page) %>%
  html_nodes(xpath = '//*[@id="ctl00_cphContent_gvwPreparations"]') %>%
  html_table(fill=TRUE) %>% 
  bind_rows %>%
  tibble()
# gives the desired informations of the first drug (not yet very structured)

read_html(page) %>%
  html_nodes(xpath = '//*[@id="ctl00_cphContent_gvwPreparations"]') %>%
  html_text %>%
  head(10)
