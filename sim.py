import json
import post
import world as ent
import random

alienVictory = False
robotVictory = False
alienDeaths = 0
robotDeaths = 0

def printWorld(world):
    print stringifyWorld(world)

def stringifyWorld(world):
    output = ""
    for row in range(0, len(world)):
        for col in range(0, len(world[row])):
            output += world[row][col]
        output += "\n"
    return output

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
            entity.move(world, newMap, enemies, entities)
            entity.attack(world, newMap, enemies, entities)
        else:
            attackOrMove = random.randint(1, 100)
            if attackOrMove <= 60:
                entity.attack(world, newMap, enemies, entities)
            else:
                entity.move(world, newMap, enemies, entities)

def update(world):
    global robotVictory
    global alienVictory
    global config
    global alienDeaths
    global robotDeaths

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

    if len(aliens) == 0:
        robotVictory = True
    if len(robots) == 0:
        alienVictory = True

    moveAttackEntities(robots, world, newMap, aliens)
    moveAttackEntities(aliens, world, newMap, robots)

    world["robots"] = []
    for robot in robots:
        robot_dict = {}
        robot_dict["row"] = robot.row
        robot_dict["col"] = robot.col
        world["robots"].append(robot_dict)

    robotDeaths = config["entities"]["robot_count"] - len(robots)

    world["aliens"] = []
    for alien in aliens:
        alien_dict = {}
        alien_dict["row"] = alien.row
        alien_dict["col"] = alien.col
        world["aliens"].append(alien_dict)

    alienDeaths = config["entities"]["alien_count"] - len(aliens)

    world["map"] = newMap

    return world

twitter = post.Twitter()
with open("auth.json", "r") as authFile:
    credentials = json.loads(authFile.read())
    twitter.init_api(credentials)

config = {}
with open("config.json", "r") as configFile:
    config = json.loads(configFile.read())

stats = {}
with open("stats.json", "r") as statsFile:
    stats = json.loads(statsFile.read())

with open("world.json", "r+") as worldFile:
    world = json.loads(worldFile.read())

    if world["reset"]:
        world = ent.generateWorld(config["map"]["height"], config["map"]["width"], config["entities"]["alien_count"], \
            config["entities"]["robot_count"], config["seed_index"])
        config["seed_index"] += 1
    else:
        world = update(world)

    output = ""
    if alienVictory and robotVictory:
        output += u'\U0001F47D' + " Stalemate " + u'\U0001F916' + "\n\nAll Time Stats\n" + u'\U0001F47D' + " Deaths: "
        output += str(stats["alien_deaths"]) + " + " + str(alienDeaths) + "\n" + u'\U0001F916' + " Deaths: "
        output += str(stats["robot_deaths"]) + " + " + str(robotDeaths)
        stats["alien_deaths"] += alienDeaths
        stats["robot_deaths"] += robotDeaths
        world["reset"] = True

    elif alienVictory:
        output += u'\U0001F47D' + " Alien Victory " + u'\U0001F47D' + "\n\nAll Time Stats\n" + u'\U0001F47D' + " Deaths: "
        output += str(stats["alien_deaths"]) + " + " + str(alienDeaths) + "\n" + u'\U0001F916' + " Deaths: "
        output += str(stats["robot_deaths"]) + " + " + str(robotDeaths)
        stats["alien_deaths"] += alienDeaths
        stats["robot_deaths"] += robotDeaths
        world["reset"] = True

    elif robotVictory:
        output += u'\U0001F916' + " Robot Victory " + u'\U0001F916' + "\n\nAll Time Stats\n" + u'\U0001F47D' + " Deaths: "
        output += str(stats["alien_deaths"]) + " + " + str(alienDeaths) + "\n" + u'\U0001F916' + " Deaths: "
        output += str(stats["robot_deaths"]) + " + " + str(robotDeaths)
        stats["alien_deaths"] += alienDeaths
        stats["robot_deaths"] += robotDeaths
        world["reset"] = True

    else:
        output += stringifyWorld(world["map"])

    world["rand_state"] = random.getstate()
    worldFile.seek(0)
    worldFile.truncate()
    json.dump(world, worldFile)

    twitter.post(output)

with open("config.json", "w") as configFile:
    json.dump(config, configFile)

with open("stats.json", "w") as statsFile:
    json.dump(stats, statsFile)
