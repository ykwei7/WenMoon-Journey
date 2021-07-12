import praw
import csv
import re
import os
import os.path
from random import shuffle

def sort_comment(comment, category, count):
    # 0 stands for negative, 1 stands for positive
    if category == 0:
        dir = "neg"
    elif category == 1:
        dir = "pos"
    elif category == 2:
        dir = "neu"
    else:
        return
    dir = "C://Users//ykwei//PycharmProjects//stockscraper//sentimentTracker//training_data//" + dir
    name = os.path.join(dir, str(count) + ".txt")
    with open(name, "w") as f:
        f.write(comment)
        f.close()

def update_count(count, category):
    if category == 0:
        dir = "neg"
    elif category == 1:
        dir = "pos"
    elif category == 2:
        dir = "neu"
    else:
        return
    dir = "C://Users//ykwei//PycharmProjects//stockscraper//sentimentTracker//training_data//" + dir
    curr_count = os.path.join(dir, "current_count.txt")
    with open(curr_count, mode="w") as f:
        f.write(str(count))
        f.close()

def get_textfile_count(category):
    if category == 0:
        dir = "neg"
    elif category == 1:
        dir = "pos"
    elif category == 2:
        dir = "neu"
    else:
        return
    dir = "C://Users//ykwei//PycharmProjects//stockscraper//sentimentTracker//training_data//" + dir
    curr_count = os.path.join(dir, "current_count.txt")
    with open(curr_count, mode="r") as f:
        lines = f.readlines()
        return int(lines[0])

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
        for i in range(len(postIDs)):
            submission = reddit.submission(id=postIDs[i])
            submission.comments.replace_more(limit=None)
            comments_list = submission.comments.list()
            shuffle(comments_list)
            for comment in comments_list:
                print(comment.body)
                print("0 for negative, 1 for positive, 2 for neutral:")
                category = int(input())
                commentCount = get_textfile_count(category)
                if isinstance(commentCount, int):
                    sort_comment(comment.body, category, commentCount)
                    commentCount = commentCount + 1
                    update_count(commentCount, category)

if __name__ == '__main__':
    SubredditScraper('investing', lim=20, sort='hot').get_posts()
