import praw

reddit = praw.Reddit('bilingual_bot')
subreddit = reddit.subreddit("canada")

for submission in subreddit.new(limit=5):
    print("Title: ", submission.title)
    print("Text: ", submission.selftext)
    print("Score: ", submission.score)
    print("---------------------------------\n")