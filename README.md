# Neptune :rocket:

Proposed Level of Achievement: **Germini**

This project aims to help stock investors have a better evaluation of stocks to purchase through the popularity and sentiment of the stock.

## Table of Contents
1. [Motivation](https://github.com/ykwei7/stockscraper/blob/main/README.md#motivation)
2. [Aim](https://github.com/ykwei7/stockscraper/blob/main/README.md#aim)
3. [User Stories](https://github.com/ykwei7/stockscraper/blob/main/README.md#user-stories)
4. [Features and Timeline](https://github.com/ykwei7/stockscraper/blob/main/README.md#features-and-timeline)
5. [Tech Stack](https://github.com/ykwei7/stockscraper/blob/main/README.md#tech-stack)
6. [Project Log](https://github.com/ykwei7/stockscraper/blob/main/README.md#project-log)


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
Reddit is utilized to scrape the post and mentions and performs a regex search for specific stock tickers.
For instance, Apple is referred often as AAPL, which our regex searches for.

```
# Loops through the posts in the subreddit to search for stock tickers
for post in subreddit:
    i = i + 1
    print(i)
    if post.link_flair_text != 'Meme':
        for stock in stockTickers.keys():
            # Refines search function of stock to be more precise
            if (re.search(r'\s+\$?' + stock + r'\$?\s+', post.selftext) or re.search(
                    r'\s+\$?' + stock + r'\$?\s+', post.title)):
                postIDs.append(post.id)
                stockDetails[stock][0] += 1
                if stock not in stockMention:
                    stockMention.append(stock)

filteredStockCount = dict()
for stock in stockMention:
    filteredStockCount[stock] = stockDetails[stock]
         
# Sorts the stock to be ordered by comment mentions
sortedStockCount = sorted(filteredStockCount.items(), key=lambda x: x[1][1], reverse=True)
# Creates the CSV file
csvFile = make_csv_file(getCurrDate())
```

This information is parsed into a dictionary and exported as a CSV file for the frontend to process.
 
###### Feature 3: Sentiment Analysis
Comments from the reddit posts are scraped and labelled with a score from 1 to 10.
This is done with machine learning where a baseline model is created with Google's Tensorflow module.

```
# Model is created with these layers
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu)) #relu refers to rectified linear function
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(2, activation=tf.nn.softmax)) #2 is number of categories to output to

# Model is compiled with an optimizer and loss function
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
              
# Training of model with x_train (training data), and y_train (true labels), and 10 cycles
epochs = 10
history = model.fit(
    x_train,
    y_train,
    epochs=epochs)
```

The model learns from training data of texts categorized into positive and negative sentiments.
It can then be used to predict a new unknown text and returns a tuple of the likelihood of this comment being negative against it being positive.

```
text = "This stock is good."
# Vectorizes texts into a vectorized array for faster processing
def vectorize_text(text):
    text = tf.expand_dims(text, -1)
    text = vectorize_layer(text)
    return np.array(text)

# Model is used to predict the positive score of this text
print(model.predict(vectorize_text(text)))
// [[0.24691352 0.7530865 ]]
```

In this case, with the current training data, the model was able to predict that the positive sentiment of 0.753,
which is subsequently scaled to a score out of 10 for easier visualization.
 
## Tech Stack
1. Reddit API (For backend web scraping)
2. HTML/CSS/Javascript (For frontend)
3. Ajax jQuery (Link information from backend to frontend)
4. Python (For backend web scraping)
5. Tensorflow (For analysing keywords for sentiment)

## Project Log
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




