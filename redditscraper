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
    month = str(current_date.month)
    if len(month) == 1:
        month = "0" + month
    filename = "orbital/log/log-" + str(current_date.day) + month + str(current_date.year) + ".csv"
    return filename


class jsonFile():

    def __init__(self, name):
        self.name = name

    def writeTo(self, stockMention):
        with open(self.name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Stock", "Mentions"])
            for key, value in stockMention:
                writer.writerow([key, value])
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
        mentionedStocks = []
        i = 0
        for post in subreddit:
            i = i + 1
            print(i)
            if post.link_flair_text != 'Meme':
                for stock in stockTickers.keys():
                    if (re.search(r'\s+\$?' + stock + r'\$?\s+', post.selftext) or re.search(
                            r'\s+\$?' + stock + r'\$?\s+', post.title)):
                        stockTickers[stock][post.id] = StockPost(post.id, post.permalink, post.ups, post.downs,
                                                                 post.num_comments, stock)

        for stock in stockTickers:
            if (len(stockTickers[stock]) > 0):
                for post in stockTickers[stock]:
                    mentionedStocks.append(stockTickers[stock][post])

        json_object = json.dumps(mentionedStocks, default=jsonDefEncoder, indent=4)
        json_string = json.loads(json_object)
        postID_list = []
        for i in range(len(json_string)):
            postID_list.append(json_string[i]["postID"])
            print(json_string[i]["postURL"])

        list_set = set(postID_list)
        # convert the set to the list
        unique_list = (list(list_set))
        stockCount = {}
        stockMention = []

        for stock in stockTickers.keys():
            stockCount[stock] = 0;

        for i in range(len(unique_list)):
            submission = reddit.submission(id=unique_list[i])
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                for stock in stockTickers.keys():
                    if re.search(stock, comment.body, re.IGNORECASE):
                        stockCount[stock] += 1
                        if stock not in stockMention:
                            stockMention.append(stock)

        FilteredstockCount = dict()
        for (key, value) in stockCount.items():
            if value != 0:
                FilteredstockCount[key] = value

        sortedStockCount = sorted(FilteredstockCount.items(), key=lambda x: x[1], reverse=True)
        csv_file = jsonFile(getCurrDate())
        csv_file.writeTo(sortedStockCount)
        print(sortedStockCount)


if __name__ == '__main__':
    SubredditScraper('wallstreetbets', lim=50, sort='hot').get_posts()
