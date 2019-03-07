import praw
import pdb
import re
import os
from google.cloud import translate
#set GOOGLE_APPLICATION_CREDENTIALS=./credentials.json

reddit = praw.Reddit('bilingual_bot')
subreddit = reddit.subreddit("canadapolitics")

translateClient = translate.Client()

def translate(source):
    sourceLanguage = translateClient.detect_language(source)["language"]

    if sourceLanguage == "en":
        return translateClient.translate(source, target_language='fr')["translatedText"]
    elif sourceLanguage == "fr":
        return translateClient.translate(source, target_language='en')["translatedText"]
    else:
        return ""

# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))


for submission in subreddit.new(limit=1):
    if submission.id not in posts_replied_to:
        reply = '**' + translate(submission.title) + '**' + '\n\n' + translate(submission.selftext)
        submission.reply(reply)
        posts_replied_to.append(submission.id)


with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")

