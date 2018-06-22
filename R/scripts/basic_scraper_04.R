# Using package RCrawler avaiable on CRAN. See https://www.sciencedirect.com/science/article/pii/S2352711017300110
# Reference: https://github.com/salimk/Rcrawler#how-to-use-rcrawler

# Script create date: 22-June-2018
# install.packages("RCrawler", dependencies = TRUE)

# load the package
library(Rcrawler)
Rcrawler(Website = "https://www.journals.elsevier.com/softwarex", no_cores = 4, no_conn = 4)

Rcrawler(Website = "https://www.journals.elsevier.com/softwarex", 
         no_cores = 4, no_conn = 4, ExtractXpathPat = c("//b"))

head(DATA)
str(INDEX)
ListProjects()
MyDATA<-LoadHTMLFiles("journals.elsevier.com-221054", type = "vector")
