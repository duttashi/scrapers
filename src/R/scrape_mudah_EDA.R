# objective: Preliminary data analysis of the scraped data from mudah.my
# required data frame: `df.final`
# required data file: `data/mudah_data.csv`
# script name: scrape_mudah_EDA.R
# script create date: 24/2/2019
# script author: ashish dutt

# clean the workspace
rm(list = ls())
# Load the data
mudah.data<- read.csv("data/mudah_data.csv", header = TRUE, sep = ",")
