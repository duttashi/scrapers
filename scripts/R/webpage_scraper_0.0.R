# Objective: To scrape children books from goodreads, https://www.goodreads.com/list/show/226.Favorite_books_from_my_childhood
# reference: http://giorasimchoni.com/2017/09/24/2017-09-24-where-my-girls-at/

library(tidyverse)
library(stringr)
library(rvest)

startUrl <- "https://www.goodreads.com/list/show/226.Favorite_books_from_my_childhood"
html <- read_html(startUrl)



bookTitles<-html %>%
  html_nodes(".bookTitle") %>%
  html_text(trim = TRUE)

html %>%
  html_nodes("a") %>%
  html_attr("href") %>%
  # remove the book/show
  discard(!str_detect(., "^/book/show")) %>%
  # remove the NAs
  na.omit()%>%
  # note the values are repetative. Keep only the unique values
  unique()

  

title <- html %>%
  html_nodes(".bookTitle") %>%
  html_text(trim = TRUE)

bookLinks <- html %>%
  html_nodes("a") %>%
  html_attr("href") %>%
  discard(!str_detect(., "^/book/show")) %>%
  na.omit() %>%
  unique()

score <- html %>%
  html_nodes("a") %>%
  html_text() %>%
  discard(!str_detect(., "score: [0-9,]+")) %>%
  str_extract("[0-9,]+") %>%
  str_replace_all(",", "") %>%
  as.numeric()

df<- tibble(title = title,
            book_Links = bookLinks,
            book_score = score
            )
head(df,5)


getBookDescription <- function(bookLink) {
  url <- str_c("https://www.goodreads.com", bookLink)
  read_html(url) %>% 
    html_node("#descriptionContainer") %>% 
    html_text() %>% trimws()
}

getBooks <- function(i) {
  cat(i, "\n")
  url <- str_c(startUrl, "?page=", i)
  
  html <- read_html(url)
  
  title <- html %>%
    html_nodes(".bookTitle") %>%
    html_text(trim = TRUE) #%>%
  #discard(!str_detect(., "[A-Z0-9]"))
  
  author <- html %>%
    html_nodes(".authorName") %>%
    html_text(trim = TRUE) %>%
    discard(str_detect(., "^\\("))
  
  rate <- html %>%
    html_nodes(".minirating") %>%
    html_text(trim = TRUE) %>%
    str_extract_all("[0-9.,]+", simplify = TRUE) %>%
    as_tibble() %>%
    magrittr::set_colnames(c("avg", "nRaters")) %>%
    mutate(nRaters = str_replace_all(nRaters, ",", "")) %>%
    mutate_all(as.numeric)
  
  score <- html %>%
    html_nodes("a") %>%
    html_text() %>%
    discard(!str_detect(., "score: [0-9,]+")) %>%
    str_extract("[0-9,]+") %>%
    str_replace_all(",", "") %>%
    as.numeric()
  
  nVoters <- html %>%
    html_nodes("a") %>%
    html_text() %>%
    discard(!str_detect(., "([0-9,]+ people voted)|(1 person voted)")) %>%
    str_extract("[0-9,]+") %>%
    str_replace_all(",", "") %>%
    as.numeric()
  
  bookLinks <- html %>%
    html_nodes("a") %>%
    html_attr("href") %>%
    discard(!str_detect(., "^/book/show")) %>%
    na.omit() %>%
    unique()
  
  bookDescription <- bookLinks %>%
    map_chr(getBookDescription)
  
  return(tibble(
    title = title,
    author = author,
    rating = rate$avg,
    nRaters = rate$nRaters,
    score = score,
    nVoters = nVoters,
    bookDescription = bookDescription
  ))
}

goodreads <- c(1:2) %>%
  map_dfr(getBooks)
