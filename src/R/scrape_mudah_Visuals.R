# objective: Data visualization for scraped and cleaned data from mudah website
# required data file: `data/mudha_data_clean.csv`
# script name: scrape_mudah_Visuals.R
# script create date: 27/2/2019
# script last modified date: 27/2/2019
# script author: ashish dutt

# clean the workspace
rm(list = ls())
# Load the data
df<- read.csv("data/mudha_data_clean.csv", header = TRUE, sep = ",")
str(df)
df$X<- NULL

# Outliers test, using cooks distance
# reference: http://r-statistics.co/Outlier-Treatment-With-R.html
mod <- lm(itemPrice ~ ., data=df)
cooksd <- cooks.distance(mod)
plot(cooksd, pch="*", cex=2, 
     main="Influential Obs by Cooks distance")  # plot cook's distance
abline(h = 4*mean(cooksd, na.rm=T), col="red")  # add cutoff line
text(x=1:length(cooksd)+1, y=cooksd, labels=ifelse(cooksd>4*mean(cooksd, na.rm=T),names(cooksd),""), col="red")  # add labels
influential <- as.numeric(names(cooksd)[(cooksd > 4*mean(cooksd, na.rm=T))])  # influential row numbers
head(df[influential, ])  # influential observations.
# Row 4,27,41,43,72,86 have very big item prices and are outliers

# Treating the outliers
## Capping method

df1 = df %>%
  group_by(itemCat) %>%
  filter(!(abs(itemPrice - median(itemPrice)) > 2*sd(itemPrice)))

######## VISUALIZING CLEAN DATA ###########

# see what fonts you have available with the command windowsFonts()
windowsFonts()
# Now, load extra fonts
#font_import() #  (it took like 15 minutes):
#loadfonts(device = "win")

# Load the required libraries
library(extrafont)
library(RColorBrewer) # for brewer.pal()
library(gridExtra) # for grid.arrange()
library(ggpubr) # for annotate_figure()
library(grid) # for grid_rect()

# CREATING A MANUAL COLOR PALETTE
mycolors = c(brewer.pal(name="Set2", n = 8), 
             brewer.pal(name="Set1", n = 6))

myFont1<- "Roboto"
myFont2<- "Lucida Console"
myFont3<- "Georgia"

# CREATE A CUSTOM THEME for Journal IEEE Access
my_theme<- function(base_size = 11, base_family = ""){
  theme_bw(base_size = base_size, base_family = base_family) %+replace%
    theme(plot.title = element_text(family=myFont1, size = 11,
                                    # where t=top margin, r=right margin, b=bottom margin, l=left margin
                                    margin = margin(t = 00, r = 0, b = 10, l = 0)
    ), # end element_text()
    plot.caption = element_text(hjust=0.5, vjust = 0.5, size=rel(1.2)),
    axis.text = element_text(family=myFont3, size = 8),
    axis.text.x = element_text(angle = 70, hjust = 0.5),
    axis.title.x = element_text(family=myFont2, size = 10,
                                margin = margin(t = 10, r = 0, b = 0, l = 0)
    ),
    axis.title.y = element_text(family=myFont2, size = 10,
                                angle = 90,
                                margin = margin(t = 0, r = 10, b = 0, l = 0)
    ),
    legend.title = element_text(family=myFont1, size = 10),
    legend.text = element_text(family=myFont1, size = 9),
    panel.border=element_rect(fill=NA, size = 1),
    legend.background = element_rect(fill="gray90", size=.5, 
                                     linetype="dotted"))
}

# create a ggplot2 object
p<-ggplot(data = df, aes(x = itemArea))
p1<- p +geom_bar(stat = "count", color="black",aes(fill = itemCat))+
  my_theme()+
  ggtitle("(A) Sale item location ")+
  scale_x_discrete(name="item location", labels= levels(df$itemArea))+
  scale_y_continuous(name = "Item Count")+
  scale_color_manual(values = mycolors)+
  scale_fill_discrete(name = "Item Type")

p2<- p +geom_bar(stat = "count", color="black",aes(fill = itemCondt))+
  my_theme()+
  ggtitle("(B) Sale item condition ")+
  scale_x_discrete(name="item location", labels= levels(df$itemArea))+
  scale_y_continuous(name = "Item Count")+
  scale_color_manual(values = mycolors)+
  scale_fill_discrete(name = "Item Condition")

# Arrange the plots in a 2x2 grid
fig1<- grid.arrange(p1,p2,ncol=2, nrow=1) # ensure the plot size is big enough, else there will be an error displayed in UseMethod("depth")

# Annotate the arranged figure
annotate_figure(fig1
                ,top = text_grob("Sale Item Distribution by Area & Condition", 
                                 color = "black", face = "bold", size = 12, family = "Arial")
                ,bottom = text_grob("Data source: \n www.mudah.my\n", color = "brown",
                                    hjust = 1, x = 1, face = "italic", size = 10, family = "Times"))
# Add a black border around the 2x2 grid plot
grid.rect(width = 1.00, height = 0.99, 
          gp = gpar(lwd = 2, col = "black", fill=NA))
# clear the graphic device
grid.newpage()
