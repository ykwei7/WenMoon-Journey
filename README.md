# Neptune :rocket:

Level of Achievement: **Apollo**

This project aims to help stock investors have a better evaluation of stocks to purchase through the popularity and sentiment of the stock.

## Table of Contents
1. [Motivation](https://github.com/ykwei7/stockscraper/blob/main/README.md#motivation)
2. [Aim & User Stories](https://github.com/ykwei7/stockscraper/blob/main/README.md#aim-and-user-stories)
3. [Features and Timeline](https://github.com/ykwei7/stockscraper/blob/main/README.md#features-and-timeline)
4. [Tech Stack](https://github.com/ykwei7/stockscraper/blob/main/README.md#tech-stack)
5. [Milestone Updates](https://github.com/ykwei7/stockscraper/blob/main/README.md#milestone-updates)
6. [Project Log](https://github.com/ykwei7/stockscraper/blob/main/README.md#project-log) 


## Motivation
In today’s age of internet finance, investing your money is just a few clicks away. With the recent GME saga, more people than ever have flocked to stock trading platforms, following the trend of bandwagon speculation. GME rose from a measly 8 USD and peaked at more than 400 USD, generating a return of up to fifty times for every dollar put in.
In this new era of investing, speculation creates demand for stocks and represents an important aspect of investing. 

Our platform aims to capitalize on this aspect to quantify, explain and predict such speculation.  Often, it is said that people invest based on emotions, and thus our platform scrapes data from social media platforms like Reddit and Twitter to ascertain and gauge trending sentiments. This allows us to identify and suggest stocks that are riding on such "hype waves", allowing us to get in on the action before it rockets.

## Aim and User Stories
Our platform aims to provide individuals who plan to purchase stocks a better evaluation of a stock.
This is done via the scraping of posts and comments on Reddit to obtain the popularity and relative sentiment score of popular upcoming stocks.
We gauge the popularity by obtaining the number of times a particular stock is mentioned and the sentiment is obtained via a machine learning model.

## Features and Timeline

###### Feature 1: Website
Our website utilizes a table to display our results in a user-friendly manner.
Relevant information such as opening and closing prices were added to gauge the trend of the stock.
A searchbar functionality was added to search for specific stock tickers.
Sorting functionality was implemented to allow users to view the top stocks for a particular category.

###### Feature 2: Webscraper
Reddit API is utilized to scrape the post and mentions and performs a regex search for specific stock tickers.
For instance, Apple is referred often as AAPL, which our regex searches for.
In this case, we scrape for the number of posts that mention this stock and binds it to its dictionary value.

```
# Loops through the posts in the subreddit to search for stock tickers
for post in subreddit:
    if post.link_flair_text != 'Meme':
	for stock in stockTickers.keys():
	    if (re.search(r'\s+\$?' + stock + r'\$?\s+', post.selftext) or re.search(
		    r'\s+\$?' + stock + r'\$?\s+', post.title)):
		postIDs.append(post.id)
		stockDetails[stock]["post_mentions"] += 1
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

###### Feature 3: Sentiment Analysis
Comments from the reddit posts are scraped and labelled with a score out of 1.
This is done with machine learning where a baseline model is created with Google's Tensorflow module.

```
# Model is created with these layers
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu)) #relu refers to rectified linear function
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(3, activation=tf.nn.softmax)) #3 is number of categories to output to

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

The model learns from training data of texts categorized into negative, positive and neutral categories.

For instance, in the code snippet below, we use the model to predict the sentiment of this statement.
Index 0,1 and 2 of the output indicates the likelihood that it belongs to negative, positive or the neutral category.
In this case, the model predicts a 52.1% chance that it belongs to the positive category and returns an index '1'.

```
x_train, y_train = load_data("training_data")
model = create_model()
train_model(model,1000,x_train,y_train)
print(predict(model, "This stock is good"))
// [0.36367467045783997, 0.5207763314247131, 0.1155489981174469]
// 1
```

This sentiment analysis is then applied onto all the comments that mention the stock as seen below
In other words, if the scraper picked up 10 comments that mentioned the stock and predicted 6 as positive.
The overall sentiment score of this stock would be 0.60.

We also included a testing feature that tests how accurate our model is.
This is done via comparing the number of correctly predicted labels against a set of comments with known labels.

## Milestone Updates
For this milestone, we launched our application using HeroKu and updated the following features:

Frontend
- Improved user interface of website
- Added a searchbar feature to search for specific stock tickers
- Added a sorting feature to sort for different categories
- Added color indicators for rising and dropping stock prices

Backend
- Scraped for closing and opening stock prices
- Added more training data for sentiment analysis
- Added a testing feature for a more accurate model
 
## Tech Stack
1. Reddit API (For backend web scraping)
2. HTML/CSS/Javascript (For frontend)
3. Ajax jQuery (Link information from backend to frontend)
4. BeautifulSoup (To scrape real-time stock prices)
5. Python (For backend web scraping)
6. Tensorflow (For analysing keywords for sentiment)

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

S/n | Task | Date | Hours | Remarks
| :---: | :---: | :---: | :---: | :---: | 
1 | Idealization | 10/5 | 4 | Came up with idea for initial prototype and ways to implement each section of idea								
2 | Poster | 13/5 | 4 | Drafted the idea for poster and implemented it with PiktoChart									
3 | Video | 13/5 | 2 | Wrote script for video and did recording to showcase features of prototype 									
4 | Adjusting backend scraping | 17/5 | 8 | Adjusted code to output in the correct json format and debugged the re.search to count for proper terms and adjusted stock namings to prevent mislabelling of stock, debugged to check if count is correct									
5 | Learning HTML and CSS | 21/5 | 8 | Read up on HTML, CSS									
6 | Brief website implementation | 25/5 | 8 | Did brief implementation of the skeleton of website and basic website features 							
7 | Create HTML Table | 28/5 | 8 | Converted scraped data into a csv file to display as a HTML table via javascript and ajax jquery						
8 | Refined search function | 04/06 | 4 | Refined search function to search for specific stock ticker keywords									
9 | Javascript | 09/06 | 8 | Read up on JS									
10 | Refined stock selection dataset | 11/06 | 8 | Changed the scope of stocks to find for the top 2000 stocks for faster processing						11 | Improved interface of website | 18/06 | 8 | Redesigned website and added new subreddit sentiments									
12 | Sentiment Analysis | 21/06, 25/06 | 14 | Implemented base model for machine learning									
13 | ReadMe | - | 4 | Updated ReadMe to include more updates on project									
14 | Making of video | 25/06 | 2 | Made video for milestone 2
15 | Improved interface of website | 08/07 | 8 | Redesigned website and improved aesthetics
16 | Sorting functionality of table | 15/07 | 12 | Combined Ajax Jquery syntax to fit for table header sorting 
17 | Search functionality | 18/07 | 4 | Allowed for search functionality for specific stock tickers
18 | Price Scraper | 21/07 | 6 | Used BeautifulSoup to scrape for stock prices
19 | Collection of training data | 21/07, 22/07 | 8 | Implemented a datasorter function and manually labeled comments
20 | Making of video & ReadMe | 26/07 | 4 | Made video and updated ReadMe for milestone 3 
	
Total hours per member: 141										


