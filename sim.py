import json
import post
twitter = post.Twitter()

with open("auth.json", "r") as authFile:
    credentials = json.loads(authFile.read())
    twitter.init_api(credentials)

with open("world.json", "r") as worldFile:
    world = json.loads(worldFile.read())
    # twitter.post(world)
