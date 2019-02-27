# objective: Predictive Analytics of the scraped data from mudah.my
# required data file: `data/mudha_data_clean.csv`
# script name: scrape_mudah_ML.R
# script create date: 26/2/2019
# script last modified date: 26/2/2019
# script author: ashish dutt

# clean the workspace
rm(list = ls())

# load the required libraries
library(plyr) # for mapvalues()
library(caret) # for nearZeroVar()
library(mice) # for missing data imputation
library(factoextra) # for fviz_cluster(), get_eigenvalue(), eclust()
library(FactoMineR) # for PCA() and MCA()
library(gridExtra) # for grid.arrange()
library(ggpubr) # for annotate_figure()
library(grid) # for grid.rect()
library(reshape2) # for melt()


# Load the data
mudah.data<- read.csv("data/mudha_data_clean.csv", header = TRUE, sep = ",")

# make a copy
df<- mudah.data
# initial exploration
dplyr::glimpse(df)
# drop title
df$X<- NULL
df$itemTitle<- NULL

# recode the categorical vars to integer but keep them as categorical
table(df$iDay)#2
table(df$iMonth) # 2
table(df$itemArea)# 12
table(df$itemCat)# 9
table(df$itemCondt)#2

df$iDay<- mapvalues(df$iDay, from = levels(df$iDay), to=c(1:2))
df$iMonth<- mapvalues(df$iMonth, from = levels(df$iMonth), to=c(1:2))
df$itemCondt<- mapvalues(df$itemCondt, from = levels(df$itemCondt), to=c(1:2))
df$itemCat<- mapvalues(df$itemCat, from = levels(df$itemCat), to=c(1:9))
df$itemArea<- mapvalues(df$itemArea, from = levels(df$itemArea), to=c(1:12))

dplyr::glimpse(df)

# check for near zero variance
badCols<- nearZeroVar(df)
dim(df[,badCols]) # There are 2 variables with near zero variance
colnames(df[,badCols]) # iDay and iMonth exhibit nzv
df.new<- df[,-badCols] # drop the nzv vars

# check for missing values
sum(is.na(df.new))

# Clustering
# Conduct the MCA test
str(df.new)
res.mca<- MCA(df.new[,c(1:4)], ncp = 5, graph = TRUE)
# visualize the percentages of inertia explained by each MCA dimensions, use the function fviz_eig() or fviz_screeplot() [factoextra package]
screeplot<-fviz_screeplot(res.mca, addlabels = TRUE,
                          barfill = "#b4a8d1", barcolor = "black",
                          ylim = c(0, 50), xlab = "Clustering tendency of categorical features", ylab = "Percentage of explained variance",
                          main = "(A) Scree plot for categorical variables"
)
# Contributions of variables to PC1
pc1<-fviz_contrib(res.mca, choice = "var", 
                  axes = 1, top = 10, sort.val = c("desc"),
                  fill = "#b4a8d1")+
  rotate_x_text(angle = 80)+
  labs(title="(B) categorical feature")

# Contributions of variables to PC2
pc2<-fviz_contrib(res.mca, choice = "var", axes = 2, top = 10,
                  sort.val = c("desc"),
                  fill = "#b4a8d1")+
  labs(title="(C) categorical feature")
fig1<- grid.arrange(arrangeGrob(screeplot), 
                    arrangeGrob(pc1,pc2, ncol=1), ncol=2, widths=c(2,1)) 
annotate_figure(fig1
                ,top = text_grob("Clustering tendency of categorical features", color = "black", face = "bold", size = 14)
                ,bottom = text_grob("Data source: www.mudah.my\n", color = "brown",
                                    hjust = 1, x = 1, face = "italic", size = 10)
)
# Add a black border around the 2x2 grid plot
grid.rect(width = 1.00, height = 0.99, 
          gp = gpar(lwd = 2, col = "black", fill=NA))

# Extract all the PC and store in a new data frame
names(df.new)
# so even though DIABETE3 is not found as an imp variable, we still add it to the dataframe as its a classification problem
df.new.impcs<-as.data.frame(df.new[,c(2:5)])
# clear the graphic device
grid.newpage()

# initial BaseLine models
smp_size <- floor(0.70 * nrow(df.new.impcs))
# set the seed to make your partition reproducible
set.seed(2019)
train_ind <- sample(seq_len(nrow(df.new.impcs)), size = smp_size)
df.train <- df.new.impcs[train_ind, ]
df.test <- df.new.impcs[-train_ind, ]

# Run algorithms using 10-fold cross validation
control <- trainControl(method="repeatedcv", number=10, repeats = 3)
metric <- "RMSE"

colnames(df.new.impcs)
# Build models
# CART
set.seed(2019)
fit.cart <- train(itemPrice ~., data=df.new.impcs, method="rpart", metric=metric, trControl=control)
# kNN 
# Note: KNN takes long time to execute
set.seed(2019)
fit.knn <- train(itemPrice~., data=df.train, method="knn", metric=metric, trControl=control)
# SVM
# Note: SVM takes a very long time to execute
#set.seed(2019)
#fit.svm <- train(itemPrice~., data=df.train, method="svmRadial", metric=metric, trControl=control)

# summarize accuracy of models
results <- resamples(list(cart=fit.cart, knn=fit.knn))
summary(results)
# compare accuracy of models
dotplot(results)

# Make Predictions using the best model 
predictions <- predict(fit.cart, df.test)
table(predictions, df.test$itemPrice)
#confusionMatrix(predictions, df.test$itemPrice)
