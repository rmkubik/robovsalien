import tweepy

class Twitter:
    def __init__(self):
        self.api = None

    def init_api(self, credentials):
        # Add your credentials to auth.json
        # run the following command to avoid committing your credentials to repo
        # git update-index --assume-unchanged auth.json
        consumer_key = ""
        consumer_secret = ""
        access_token = ""
        access_token_secret = ""

        consumer_key = credentials["consumer_key"]
        consumer_secret = credentials["consumer_secret"]
        access_token = credentials["access_token"]
        access_token_secret = credentials["access_token_secret"]

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(auth)

    def post(self, world):
        output = ""
        for row in range(0, len(world["map"])):
            for col in range(0, len(world["map"][row])):
                output += world["map"][row][col]
            output += "\n"
        self.api.update_status(output);
