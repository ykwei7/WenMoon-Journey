# Neptune :rocket:

Proposed Level of Achievement: **Germini**

This project aims to help stock investors have a better evaluation of stocks to purchase through the popularity and sentiment of the stock.

## Table of Contents
1. [Motivation](https://github.com/ykwei7/stockscraper/blob/main/README.md#motivation)
2. [Aim](https://github.com/ykwei7/stockscraper/blob/main/README.md#aim)
3. [User Stories](https://github.com/ykwei7/stockscraper/blob/main/README.md#user-stories)
4. [Features and Timeline](https://github.com/ykwei7/stockscraper/blob/main/README.md#features-and-timeline)
5. [Tech Stack](https://github.com/ykwei7/stockscraper/blob/main/README.md#tech-stack)
6. [Additional Info](https://github.com/ykwei7/stockscraper/blob/main/README.md#additional-info)


## Motivation
In today’s age of internet finance, investing your money is just a few clicks away. With the recent GME saga, more people than ever have flocked to stock trading platforms, following the trend of bandwagon speculation. GME rose from a measly 8 USD and peaked at more than 400 USD, generating a return of up to fifty times for every dollar put in.
In this new era of investing, speculation creates demand for stocks and represents an important aspect of investing. 

Our platform aims to capitalize on this aspect to quantify, explain and predict such speculation.  Often, it is said that people invest based on emotions, and thus our platform scrapes data from social media platforms like Reddit and Twitter to ascertain and gauge trending sentiments. This allows us to identify and suggest stocks that are riding on such "hype waves", allowing us to get in on the action before it rockets.

## Aim
This platform aims to scrape data from Reddit and Twitter to find trending stocks before it rises sharply. 

## User Stories
As an investor, data on potential trending stocks is useful for a better evaluation of the stock.

## Features and Timeline

###### Feature 1: Website
The website serves as an interface to display results of our web scraper. 
HTML is utilized to create the base skeleton of the website, including a basic ABOUT US page.
Ajax jQuery and javascript is used to link the backend information (Stock mentions etc) to the frontend.
CSS is used to do stying to provide better navigation and user experience.

###### Feature 2: Webscraper
Reddit is utilized to scrape the post and mentions and performs a regex search for specific stock ticker keys.
For instance, Apple is referred often as AAPL, which our regex searches for.

```
for post in subreddit:
    i = i + 1
    print(i)
    if post.link_flair_text != 'Meme':
        for stock in stockTickers.keys():
            if (re.search(r'\s+\$?' + stock + r'\$?\s+', post.selftext) or re.search(
                    r'\s+\$?' + stock + r'\$?\s+', post.title)):
                postIDs.append(post.id)
                stockDetails[stock][0] += 1
                if stock not in stockMention:
                    stockMention.append(stock)
```

This information is parsed into a dictionary and exported as a CSV file for the frontend to process.
 
###### Feature 3: Sentiment Analysis






###### Features to be completed by the mid of July      
1. Use machine learning to improve accuracy of sentiment analysis to interpret human language and emotion
 
## Tech Stack
1. Reddit API
2. HTML/CSS/Javascript (For frontend)
3. Python (For backend web scraping)
4. Tensorflow (For analysing keywords for sentiment)

<!-- 
Additional features to look at:
1. Rate of increase of upvotes and commenting over time that determines popularity
2. Length of comments to prevent bot manipulation 
3. Whether to ignore penny stock mentions  
4. Analysis of mentions to price movement correlation 
5. Machine learning AI to pick up on sentiment heavy keywords  
6. Pick up on stock sentiments of key players in the stock market e.g Elon Musk and give higher weightage  
7. Scrape data from other websites such as Twitter/4Chan 
8. DD tagged post - More weightage based on length 
-->




