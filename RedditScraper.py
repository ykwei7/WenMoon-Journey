import praw
import csv
import re
import json
import datetime
from sentimentTracker.sentimentTracker import predict
from tensorflow import keras
from PriceScraper import stock_price

class StockComment(object):
    def __init__(self, stock, numComments):
        self.stock = stock
        self.numComments = numComments

    def jsonEnc(self):
        return {'stock' : self.stock, 'numComments' : self.numComments}

class StockPost(object):
    def __init__(self, postID, postURL, ups, downs, numComments, stock):
        self.postID = postID
        self.url = postURL
        self.stock = stock
        self.ups = ups
        self.downs = downs
        self.numComments = numComments

    def jsonEnc(self):
        return {'stock': self.stock, 'postID': self.postID, 'postURL': self.url, 'ups': self.ups, 'downs': self.downs,
                'numComments': self.numComments}

def jsonDefEncoder(obj):
    if hasattr(obj, 'jsonEnc'):
        return obj.jsonEnc()
    else:  # some default behavior
        return obj.__dict__

def getFilename(subreddit):
    current_date = datetime.datetime.now()
    date = str(current_date.day)
    month = str(current_date.month)
    year = str(current_date.year)
    if len(date) == 1:
        date = "0" + date
    if len(month) == 1:
        month = "0" + month
    dir = "orbital/log/"
    filename = "{dir}{subreddit}_log-{date}{month}{year}.csv".format(dir=dir, subreddit=subreddit,date=date,month=month,year=year)
    return filename


class csvFile():

    def __init__(self, name):
        self.name = name

    def writeTo(self, sortedStocks, stockMentions):
        with open(self.name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Stock","Previous Close", "Opening Price", "Post Mentions", "Comment Mentions", "Sentiment score","Change"])
            for stock in sortedStocks:
                value = stockMentions[stock]
                writer.writerow([stock, value["prices"][1], value["prices"][0], value["post_mentions"],
                    value["comment_mentions"], value["sentiment_score"], value["prices"][2]])
            file.close()

class SubredditScraper:

    def __init__(self, sub, sort='new', lim=900):
        self.sub = sub
        self.sort = sort
        self.lim = lim

        print(
            f'SubredditScraper instance created with values '
            f'sub = {sub}, sort = {sort}, lim = {lim}')

    def set_sort(self):
        if self.sort == 'new':
            return self.sort, reddit.subreddit(self.sub).new(limit=self.lim)
        elif self.sort == 'top':
            return self.sort, reddit.subreddit(self.sub).top(limit=self.lim)
        elif self.sort == 'hot':
            return self.sort, reddit.subreddit(self.sub).hot(limit=self.lim)
        else:
            self.sort = 'hot'
            print('Sort method was not recognized, defaulting to hot.')
            return self.sort, reddit.subreddit(self.sub).hot(limit=self.lim)

    def get_posts(self):
        stockTickers = {}
        with open('tickers.csv', mode='r') as infile:
            reader = csv.reader(infile)
            for row in reader:
                stockTickers[row[0].split(',')[0]] = {}
        """Get unique posts from a specified subreddit."""

        # Attempt to specify a sorting method.
        sort, subreddit = self.set_sort()

        print(f'Collecting information from r/{self.sub}.')
        postIDs = []
        stockDetails = {}

        for stock in stockTickers.keys():
            stockDetails[stock] = {}
            stockDetails[stock]["post_mentions"] = 0
            stockDetails[stock]["comment_mentions"] = 0
            stockDetails[stock]["sentiment_score"] = 0
            stockDetails[stock]["scores"] = [0,0,0]
            stockDetails[stock]["prices"] = 0


        stockMention = []
        i = 0
        for post in subreddit:
            i = i + 1
            print(i)
            if post.link_flair_text != 'Meme':
                for stock in stockTickers.keys():
                    if (re.search(r'\s+\$?' + stock + r'\$?\s+', post.selftext) or re.search(
                            r'\s+\$?' + stock + r'\$?\s+', post.title)):
                        # stockTickers[stock][post.id] = StockPost(post.id, post.permalink, post.ups, post.downs,
                        #                                          post.num_comments, stock)
                        postIDs.append(post.id)
                        stockDetails[stock]["post_mentions"] += 1
                        if stock not in stockMention:
                            stockMention.append(stock)

        path = "sentimentTracker/stock_model"
        model = keras.models.load_model(path)

        print("Model loaded.")
        print("Scraping comments from PostIDs:")
        postIDs = list(set(postIDs))
        for i in postIDs:
            print(i)

        for i in range(len(postIDs)):
            submission = reddit.submission(id=postIDs[i])
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                for stock in stockTickers.keys():
                    if re.search(r'\s+\$?' + stock + r'\$?\s+', comment.body):
                        stockDetails[stock]["comment_mentions"] += 1
                        # prediction returns a index where 0,1,2 stands for neg,pos,neu
                        prediction = predict(model, comment.body)
                        # print(f"{comment.body} :\n{prediction}")
                        stockDetails[stock]["scores"][prediction] += 1
                        if stock not in stockMention:
                            stockMention.append(stock)

        filteredStockCount = dict()
        print("Obtaining sentiment score and scraping prices...")
        for stock in stockMention:
            scores = stockDetails[stock]["scores"]
            # formula to calc scores can be adjusted
            # print(f"{scores[0]} , {scores[1]}")
            neg_score = scores[0]
            pos_score = scores[1]
            neu_score = scores[2]

            if (neg_score + pos_score) != 0:
                sentiment = round((pos_score / (neg_score + pos_score)), 2)
            else:
                sentiment = 0
            stockDetails[stock]["sentiment_score"] = sentiment
            filteredStockCount[stock] = stockDetails[stock]
            filteredStockCount[stock]["prices"] = stock_price(stock)

        print(filteredStockCount)
        sortedStockCount = sorted(filteredStockCount)
        print(sortedStockCount)
        csv_file = csvFile(getFilename(self.sub))
        csv_file.writeTo(sortedStockCount, filteredStockCount)

if __name__ == '__main__':
    SubredditScraper('stocks', lim=100, sort='hot').get_posts()
    SubredditScraper('investing', lim=100, sort='hot').get_posts()
    SubredditScraper('wallstreetbets', lim=100, sort='hot').get_posts()
