
###### Alternate approach # 1
# Reference: https://stackoverflow.com/questions/36683510/r-web-scraping-across-multiple-pages

library(tidyverse)
library(rvest)
url_base<- "https://www.eliteprospects.com/draft/nhl-entry-draft/"
map_df(2017:2018, function(i) {
  
  # simple but effective progress indicator
  cat(".")
  pg <- read_html(sprintf(url_base, i))
  
  data.frame(
    
    team = html_text(html_nodes(pg, ".team")),
    player = html_text(html_nodes(pg, "#drafted-players .player")),
    seasons = html_text(html_nodes(pg, ".seasons")),
    GP = html_text(html_nodes(pg, "#drafted-players .gp")),
    G = html_text(html_nodes(pg, "#drafted-players .g")),
    A = html_text(html_nodes(pg, "#drafted-players .a")),
    TP = html_text(html_nodes(pg, "#drafted-players .tp")),
    PIM = html_text(html_nodes(pg, ".pim"))
  )
  })-> draft_data
View(draft_data)


###### Alternate approach # 2
# Reference: https://stackoverflow.com/questions/40666406/loop-across-multiple-urls-in-r-with-rvest?noredirect=1&lq=1
counter<- seq(2014, 2018, by=1)
pg<- paste("https://www.eliteprospects.com/draft/nhl-entry-draft/", counter)

myList<- lapply(url_base, function(i) {
  webpage <- read_html(i)
  # simple but effective progress indicator
  #cat(".")
  #draft_table <- html_nodes(webpage, ".team")
  #draft <- html_text(draft_table)
  team = html_text(html_nodes(webpage, ".team"))
  player = html_text(html_nodes(pg, "#drafted-players .player"))
  seasons = html_text(html_nodes(pg, ".seasons"))
  GP = html_text(html_nodes(pg, "#drafted-players .gp"))
  G = html_text(html_nodes(pg, "#drafted-players .g"))
  A = html_text(html_nodes(pg, "#drafted-players .a"))
  TP = html_text(html_nodes(pg, "#drafted-players .tp"))
  PIM = html_text(html_nodes(pg, ".pim"))
  }
  )

mydf

finaldf <- do.call(rbind, dfList) 
finaldf
