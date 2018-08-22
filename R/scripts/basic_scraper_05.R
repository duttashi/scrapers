library(tidyverse)
library(rvest)

base_url <- "https://www.nhs.uk/service-search/Hospital/LocationSearch/7/ConsultantResults?Specialty="

# change the code to pull other specialities
specialty_code = 230 # ie. Anaesthesia services = 230

# show 100 per page    
tgt_url <- str_c(base_url,specialty_code,"&ResultsPerPage=100&CurrentPage=")

pg <- read_html(tgt_url)

# count the total results and set the page count
res_cnt <- pg %>% html_nodes('.fcresultsinfo li:nth-child(1)') %>% html_text() %>% str_remove('.* of ') %>% as.numeric()
pg_cnt = ceiling(res_cnt / 100)

res_all <- NULL
for (i in 1:pg_cnt) {
  
  pg <- read_html(str_c(tgt_url,i))
  res_pg <- tibble(
    consultant_name = pg %>% html_nodes(".consultants-list h2 a") %>% html_text(),
    gmc_no = pg %>% html_nodes(".consultants-list .name-number p") %>% html_text() %>% 
      str_remove("GMC membership number: "),
    speciality = pg %>% html_nodes(".consultants-list .specialties ul") %>% 
      html_text() %>% str_replace_all(', \r\n\\s+',', ') %>% str_trim(),
    location = pg %>% html_nodes(".consultants-list .consultant-services ul") %>%
      html_text() %>% str_replace_all(', \r\n\\s+',', ') %>% str_trim(),
    src_link = pg %>% html_nodes(".consultants-list h2 a") %>% html_attr('href')
  ) 
  
  res_all <- res_all %>% bind_rows(res_pg)
  
}
res_all
nrow(res_all)
res_all %>% select(1:4) %>% tail()
