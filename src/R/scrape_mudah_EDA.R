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

# Load the required libraries
library(tidyverse)

# Basic EDA

# split ItemDateTime variable to ItemDate and ItemTime
df <- separate(mudah.data, col = itemDateTime, into = c("iDate", "iTime"),sep = ",")
# replace value "today" with current date in iDate
df<- df %>%
  mutate(iDate=replace(iDate, iDate=="today",date()))
# remove the time in iDate
df<- df %>%
  mutate(iDate=replace(iDate, iDate=="Mon Feb 25 09:13:34 2019","Mon Feb 25 2019"))

# Extract the day, month, year, time from iDate
str(df$iDate)
