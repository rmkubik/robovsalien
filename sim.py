import json
import post
import world as ent
def update(world):
    robots = []
    aliens = []

    for robot in world["robots"]:
        robots.append(ent.Entity(robot["row"], robot["col"], "robot"))

    for alien in world["aliens"]:
        aliens.append(ent.Entity(alien["row"], alien["col"], "alien"))
twitter = post.Twitter()

with open("auth.json", "r") as authFile:
    credentials = json.loads(authFile.read())
    twitter.init_api(credentials)

with open("world.json", "r") as worldFile:
    world = json.loads(worldFile.read())
    update(world)
    # twitter.post(world)
