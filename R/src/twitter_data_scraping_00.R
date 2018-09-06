library(rtweet)

# Note: As per the documentation, you'll need to authenticate the twitter account api first. Once authentication is done, there is no need to do it each time you execute the program, unlike in python this is a must process.
## search for 18000 tweets using the rstats hashtag
rt <- search_tweets(
  "#Malaysia", n = 1800, include_rts = FALSE
)
ts_plot(rt, "3 hours") +
  ggplot2::theme_minimal() +
  ggplot2::theme(plot.title = ggplot2::element_text(face = "bold")) +
  ggplot2::labs(
    x = NULL, y = NULL,
    title = "Frequency of #rstats Twitter statuses from past 9 days",
    subtitle = "Twitter status (tweet) counts aggregated using three-hour intervals",
    caption = "\nSource: Data collected from Twitter's REST API via rtweet"
  )
