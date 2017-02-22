import json
import post
import world as ent
import random

def moveAttackEntities(entities):
    for entity in entities:
        attackAndMove = random.randint(1, 100)
        if attackAndMove <= 30:
            # attack & move
            entity.move()
            entity.attack()
        else:
            attackOrMove = random.randint(1, 100)
            if attackOrMove <= 60:
                # attack
                entity.attack()
            else:
                # move
                entity.move()

def update(world):
    random.seed(world["seed"])
    robots = []
    aliens = []

    for robot in world["robots"]:
        robots.append(ent.Entity(robot["row"], robot["col"], "robot"))

    for alien in world["aliens"]:
        aliens.append(ent.Entity(alien["row"], alien["col"], "alien"))

    moveAttackEntities(robots)
    moveAttackEntities(aliens)

twitter = post.Twitter()

with open("auth.json", "r") as authFile:
    credentials = json.loads(authFile.read())
    twitter.init_api(credentials)

with open("world.json", "r") as worldFile:
    world = json.loads(worldFile.read())
    update(world)
    # twitter.post(world)
