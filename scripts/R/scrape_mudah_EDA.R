# objective: Exploratory data analysis of the scraped data from mudah.my
# required data file: `data/mudah_data.csv`
# script name: scrape_mudah_EDA.R
# script create date: 24/2/2019
# script last modified date: 26/2/2019
# script author: ashish dutt

# clean the workspace
rm(list = ls())
# Load the data
mudah.data<- read.csv("data/mudah_data.csv", header = TRUE, sep = ",")

# Load the required libraries
library(tidyverse)
library(RColorBrewer) # for brewer.pal()
library(VIM)

# Basic EDA

# split ItemDateTime variable to ItemDate and ItemTime
df <- separate(mudah.data, col = itemDateTime, into = c("iDate", "iTime"),sep = ",")
# replace value "today" with current date in iDate
df<- df %>%
  mutate(iDate=replace(iDate, iDate=="today",date()))
# remove the time in iDate
df<- df %>%
  mutate(iDate=replace(iDate, iDate=="Tue Feb 26 13:52:11 2019","Tue Feb 26 2019"))
# Separate the day, month, year, time from iDate
df<-separate(df, col = iDate, into = c("iDay","iMonth","iDate","iYear"),
                      sep = " ")
table(df$iYear) # constant value drop it
table(df$iDate)# constant value drop it
table(df$iDay) # variance, dont drop
table(df$iMonth) # variance, dont drop
table(df$iTime) # variance, dont drop

# dropping cols iYear, iDay, iDate
# reference: https://stackoverflow.com/questions/35839408/r-dplyr-drop-multiple-columns
df.new<- df %>%
  select(-c(iYear,iDate))

# Look & clean the other variables like itemArea, itemCat, itemCondt
table(df.new$itemCat) # categories like Full-time,Johor,Kuala Lumpur,Kelantan,Melaka,Pahang,Part-time,Penang, Perak,Putrajaya, Sabah, Selangor don't make sense.
                      # Aggregrating these categories into miscellaneous
# collapse levels in variable itemCat
levels(df.new$itemCat)<- list(
  Misc = c("Full-time","Johor","Kelantan","Kuala Lumpur","Melaka","Negeri Sembilan","Pahang",
           "Part-time","Penang","Perak","Putrajaya","Sabah","Selangor",
           "Freelance","Internship","Business for Sale","Jobs",
           "Contract","Food","Others"),
  
  Acesory = c("Accessories for Phones & Gadgets","Car Accessories & Parts",
                  "Computers & Accessories","Motorcycle Accessories & Parts",
                  "Other Accessories & Parts","Watches & Fashion Accessories"
                  ),
  Gadgets = c("Cameras & Photography","Mobile Phones & Gadgets",
              "TV/Audio/Video","Games & Consoles"),
  HomEqp = c("Bed & Bath","Furniture & Decoration","Home Appliances & Kitchen",
                  "Garden Items"),
  GenEqp = c("Air Conditioning","Hobby & Collectibles",
                 "Music Instruments","Professional/Business Equipment"),
  Vehicles = c("Commercial Vehicle & Boats","Motorcycles"),
  Clothing = c("Clothes","Shoes"),
  GenSvc = c("Cleaning","Events","Tutoring","Pest Control","Moms & Kids","Pets","Plumbing",
                  "Printing","Renovation","Sports & Outdoors",
                  "Tours and Holidays","Transport","Wedding"),
  HlthSrvc = c("Health & Beauty")
  )
levels(df.new$itemCat)
table(df.new$itemCat)

# clean the itemCondt column
# replace 'Second-Hand','Pre-owned' with 'Used'
levels(df.new$itemCondt)
table(df.new$itemCondt)

levels(df.new$itemCondt)<- list(
  New = c("New"),
  Used = c("Pre-owned (Used)","Second-hand (Used)","Used")
)
# Look at the data structure
str(df.new)

# Visualize missing data 
aggr_plot <- aggr(df.new, col=c('navyblue','red'), numbers=TRUE, sortVars=TRUE, 
                  labels=names(df.new), cex.axis=.7, gap=3, ylab=c("Histogram of missing data","Pattern"))

# Impute missing values with Predictive Mean Matching
library(mice)
tempData <- mice(df.new,m=5,maxit=5,method='pmm',seed=500)
summary(tempData)
# complete data
df.cmplt<- mice::complete(tempData,2)
colSums(is.na(df.cmplt))

dim(df.cmplt) # 20,500 adverts in 8 columns
# write the clean file to disk
write.csv(df.cmplt,"data/mudha_data_clean.csv")

# Cross Tab
library(Hmisc)
summary(~., data = df.cmplt, fun = table)
# max ads are from KL (23% n=4613) then Kedah (22% n=4612), Selangor(12%, n=2555), Penang(10% 2052)
# max ads are in Car Accessories & Parts category(31% n=6354), Clothes(13%, n=2607), Home Appliances & Kitchen(10%, n=2076), Jobs(8%, n=1564), Sports & Outdoors(8%, n=1561) 
# max ads are for New items(68% n=13850) followed by Used items(32% n=6650)
# There are 1080 ads priced over a million, possible outliers. check further
boxplot(df.cmplt$itemPrice)
str(df.cmplt)


table(df.cmplt$itemPrice)
table(df.cmplt$iMonth)
table(df.cmplt$itemArea) 
table(df.cmplt$iTime) # 20,000 ads posted between 9:57 am to 9:59 am on 26th Feb 2019
table(df.cmplt$itemArea, df.cmplt$iTime) # Kedah posted highest number of ads between 9:57-958 am, followed by KL
table(df.cmplt$itemArea, df.cmplt$itemCat) # KL posted max adverts in "Car accessories & parts" followed by Kedah


