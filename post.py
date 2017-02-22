import tweepy
import json

# Add your credentials to auth.json
# run the following command to avoid committing your credentials to repo
# git update-index --assume-unchanged auth.json
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

# load authentication information from auth.json
with open("auth.json", "r") as authFile:
    parsed_auth = json.loads(authFile.read())
    consumer_key = parsed_auth["consumer_key"]
    consumer_secret = parsed_auth["consumer_secret"]
    access_token = parsed_auth["access_token"]
    access_token_secret = parsed_auth["access_token_secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

api.update_status("Hello world!");
