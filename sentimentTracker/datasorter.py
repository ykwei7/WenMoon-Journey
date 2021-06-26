import praw
import csv
import re
import os
import os.path

def sort_comment(comment, category, count):
    # 0 stands for negative, 1 stands for positive

    if category == 0:
        dir = "neg"
    else:
        dir = "pos"
    dir = "C://Users//ykwei//PycharmProjects//stockscraper//sentimentTracker//training_data//" + dir
    name = os.path.join(dir, str(count) + ".txt")
    file1 = open(name, "w")
    file1.write(comment)
    file1.close()

reddit = praw.Reddit(
    client_id="d5ihZsiHFZKsiA",
    client_secret="FT9oMbbsY8rzN_e-CLJbrFXspWudFw",
    password="TestPassword123!",
    user_agent="Testing_api",
    username="neptuneorbit10",
)

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
        print(f"Obtaining post mentions from r/{self.sub}...")
        for post in subreddit:
            i = i + 1
            print(i)
            if post.link_flair_text != 'Meme':
                for stock in stockTickers.keys():
                    if (re.search(r'\s+\$?' + stock + r'\$?\s+', post.selftext) or re.search(
                            r'\s+\$?' + stock + r'\$?\s+', post.title)):

                        postIDs.append(post.id)
                        stockDetails[stock][0] += 1

        print("Obtaining comment mentions from posts...")
        commentCount = 0
        for i in range(len(postIDs)):
            submission = reddit.submission(id=postIDs[i])
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                print(comment.body)
                print("0 for negative, 1 for positive:")
                category = input()
                sort_comment(comment.body,category,commentCount)
                commentCount+=1
if __name__ == '__main__':
    SubredditScraper('stocks', lim=10, sort='hot').get_posts()