import praw
import csv
import re
import json
import datetime
import pandas as pd

reddit = praw.Reddit(
    client_id="d5ihZsiHFZKsiA",
    client_secret="FT9oMbbsY8rzN_e-CLJbrFXspWudFw",
    password="TestPassword123!",
    user_agent="Testing_api",
    username="neptuneorbit10",
)

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

def getCurrDate():
    current_date = datetime.datetime.now()
    date = str(current_date.day)
    month = str(current_date.month)
    year = str(current_date.year)
    if len(date) == 1:
        date = "0" + date
    if len(month) == 1:
        month = "0" + month
    dir = "orbital/log/"
    filename = dir + "log-" + date + month + year + ".csv"
    return filename


class jsonFile():

    def __init__(self, name):
        self.name = name

    def writeTo(self, stockMention):
        with open(self.name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Stock", "Post Mentions", "Comment Mentions"])
            for key, value in stockMention:
                writer.writerow([key, value[0], value[1]])
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
            # index 0 refers to post mentions, index 1 refers to comment mentions
            stockDetails[stock] = [0, 0]


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
                        stockDetails[stock][0] += 1
                        if stock not in stockMention:
                            stockMention.append(stock)

        for i in postIDs:
            print(i)

        for i in range(len(postIDs)):
            submission = reddit.submission(id=postIDs[i])
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                for stock in stockTickers.keys():
                    if re.search(r'\s+\$?' + stock + r'\$?\s+', comment.body):
                        stockDetails[stock][1] += 1
                        if stock not in stockMention:
                            stockMention.append(stock)


        filteredStockCount = dict()
        for stock in stockMention:
            filteredStockCount[stock] = stockDetails[stock]

        print(filteredStockCount)
        sortedStockCount = sorted(filteredStockCount.items(), key=lambda x: x[1][1], reverse=True)
        csv_file = jsonFile(getCurrDate())
        csv_file.writeTo(sortedStockCount)
        print(sortedStockCount)

if __name__ == '__main__':
    SubredditScraper('stocks', lim=5, sort='hot').get_posts()
