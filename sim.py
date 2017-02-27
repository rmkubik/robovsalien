import json
import post
import world as ent
import random

def printWorld(world):
    output = ""
    for row in range(0, len(world)):
        for col in range(0, len(world[row])):
            output += world[row][col]
        output += "\n"
    print output

def explosionTick(newMap):
    for row in range(0, world["height"]):
        for col in range(0, world["width"]):
            if newMap[row][col] == ent.Tiles.Explosion:
                fireChance = random.randint(1, 100)
                if fireChance <= 35:
                    newMap[row][col] = ent.Tiles.Fire
                else:
                    newMap[row][col] = ent.Tiles.Burned

def moveAttackEntities(entities, world, newMap, enemies):
    for entity in entities:
        attackAndMove = random.randint(1, 100)
        if attackAndMove <= 30:
            # attack & move
            entity.move(world, newMap, enemies, entities)
            entity.attack(world, newMap, enemies, entities)
        else:
            attackOrMove = random.randint(1, 100)
            if attackOrMove <= 60:
                # attack
                entity.attack(world, newMap, enemies, entities)
            else:
                # move
                entity.move(world, newMap, enemies, entities)

def update(world):
    if (world["rand_state"] == None):
        random.seed(world["seed"])
    else:

        random.setstate((world["rand_state"][0], tuple(world["rand_state"][1]), world["rand_state"][2]))

    robots = []
    aliens = []

    newMap = [[None for row in range(0, world["height"])] for col in range(0, world["width"])]
    for row in range(0, world["height"]):
        for col in range(0, world["width"]):
            newMap[row][col] = world["map"][row][col]

    explosionTick(newMap)

    for robot in world["robots"]:
        robots.append(ent.Entity(robot["row"], robot["col"], ent.Tiles.Robot))

    for alien in world["aliens"]:
        aliens.append(ent.Entity(alien["row"], alien["col"], ent.Tiles.Alien))

    moveAttackEntities(robots, world, newMap, aliens)
    moveAttackEntities(aliens, world, newMap, robots)

    world["robots"] = []
    for robot in robots:
        robot_dict = {}
        robot_dict["row"] = robot.row
        robot_dict["col"] = robot.col
        world["robots"].append(robot_dict)

    world["aliens"] = []
    for alien in aliens:
        alien_dict = {}
        alien_dict["row"] = alien.row
        alien_dict["col"] = alien.col
        world["aliens"].append(alien_dict)

    world["map"] = newMap

    return world

twitter = post.Twitter()

with open("auth.json", "r") as authFile:
    credentials = json.loads(authFile.read())
    twitter.init_api(credentials)

with open("world.json", "r+") as worldFile:
    world = json.loads(worldFile.read())
    # printWorld(world["map"])
    world = update(world)
    printWorld(world["map"])
    print world["aliens"]
    print world["robots"]
    world["rand_state"] = random.getstate()
    worldFile.seek(0)
    worldFile.truncate()
    json.dump(world, worldFile)
    # twitter.post(world)
