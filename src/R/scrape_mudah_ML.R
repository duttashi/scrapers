# objective: Predictive Analytics of the scraped data from mudah.my
# required data file: `data/mudha_data_clean.csv`
# script name: scrape_mudah_ML.R
# script create date: 26/2/2019
# script last modified date: 26/2/2019
# script author: ashish dutt

# clean the workspace
rm(list = ls())
# Load the data
mudah.data<- read.csv("data/mudha_data_clean.csv", header = TRUE, sep = ",")

# make a copy
df<- mudah.data

