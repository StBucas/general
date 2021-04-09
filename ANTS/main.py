import sys
import random
import pygame as p

'''
Display settings
'''
p.init()
clock = p.time.Clock()

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280
ANT_HEIGHT = 6
ANT_WIDTH = 9
MAX_ENTITIES = 70000  # number represents (number of ants) * (number of food)
screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
p.display.set_caption("Ants")
FPS = 30
IMAGES = {}

ant_group = p.sprite.Group()
entityTypes = [["A1", "A2", "A3", ],
               ["F2"], ]
activeFood = []


################################
#   | -------------------- |   #
#   |    SIM ADJUSTMENTS   |   #
#   v -------------------- v   #
################################

NUMBER_OF_ANTS_AT_START = 100
NUMBER_OF_FOOD_AT_START = 100

MAX_FOOD = 100
MAX_ANTS = 500

FOOD_PER_TICK = 2

ANT_MOVE_PER_TICK = 3
WANDER = 5
ANT_SIGHT_RADIUS = 100

ANT_LIFESPAN = 200
MATURITY = 50
FOOD_PICK_UP_LIFESPAN_INCREASE = 50

ENERGY_REQUIREMENT_TO_REPRODUCE = 201
NUMBER_OF_OFFSPRING = 35


'''
Loads images for ants and food
'''


def loadImages():

    for entities in entityTypes:
        for entitySubtype in entities:
            if entitySubtype[0] == "A":  # Loads images for ant states
                IMAGES[entitySubtype] = p.transform.scale(p.image.load(
                    "images/"+entitySubtype+".png").convert_alpha(), (ANT_WIDTH, ANT_HEIGHT))
            elif entitySubtype[0] == "F":  # Loads images for ant states
                IMAGES[entitySubtype] = p.transform.scale(p.image.load(
                    "images/"+entitySubtype+".png").convert_alpha(), (5, 5))


'''
Food class 
'''


class Food(p.sprite.Sprite):
    def __init__(self, type, pos_x, pos_y):
        self.image = IMAGES[type]
        self.rect = self.image.get_rect()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = p.Rect(pos_x, pos_y, 3, 3)


'''
ANT CLASS
@ state - which image is used
@ pos_x - X coordinate
@ pos_y - Y coordinate

'''


class Ant(p.sprite.Sprite):
    def __init__(self, state, pos_x, pos_y):
        super().__init__()
        self.image = IMAGES[state]
        self.rect = self.image.get_rect()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.lifespan = ANT_LIFESPAN
        self.age = 0  # number of ticks ant has been alive
        # closest food is initiated at 0 but will be set to instance of Food class
        self.closestFood = 0
        self.distance = 1  # distance to food

# creates ant of random type at random location

    def createAntsRandom():
        new_ant = Ant(random.choice(entityTypes[0]), random.randint(
            0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        return new_ant
# creates ant of specific type at origin

    def createAntsOrigin():
        new_ant = Ant("A2", SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        return new_ant

# moves towards food with some chamce of "wander"

    def move(ant):

        food = ant.closestFood
        distance = ant.distance

        if distance <= ANT_MOVE_PER_TICK:
            ant.pos_x = food.pos_x
            ant.pos_y = food.pos_y

        elif random.randint(1, WANDER) == 1:
            ant.pos_x += random.randint(-ANT_MOVE_PER_TICK, ANT_MOVE_PER_TICK)
            ant.pos_y += random.randint(-ANT_MOVE_PER_TICK, ANT_MOVE_PER_TICK)

        elif distance >= ANT_SIGHT_RADIUS:
            ant.pos_x += random.randint(-ANT_MOVE_PER_TICK,
                                        ANT_MOVE_PER_TICK)
            ant.pos_y += random.randint(-ANT_MOVE_PER_TICK,
                                        ANT_MOVE_PER_TICK)

        else:
            dist_ratio = ANT_MOVE_PER_TICK / distance

            ant.pos_x = ((1 - dist_ratio)*ant.pos_x +
                         (dist_ratio*food.pos_x))
            ant.pos_y = ((1 - dist_ratio)*ant.pos_y +
                         (dist_ratio*food.pos_y))

        # slope = ((food.pos_x - ant.pos_x) /
        #          (food.pos_y - ant.pos_y)**2)**(1/2)
        # ant.angle = math.atan2(
        #     x_travel, y_travel) * 180 / math.pi


'''
Creates x ants at the origin and y food scattered around for initial setup
'''


def setup(x, y):
    for i in range(x):
        ant_group.add(Ant.createAntsOrigin())
    for i in range(y):
        new_food = Food("F2", random.randint(
            0, 1280), random.randint(0, 720))
        activeFood.append(new_food)


'''
creates random Food instances if number of entities and number of food are not exceeded
'''


def chanceOfFood(x):
    if len(activeFood) * len(ant_group) < MAX_ENTITIES:
        if len(activeFood) < MAX_FOOD:
            for i in range(x):
                new_food = Food("F2", random.randint(
                    0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
                activeFood.append(new_food)


'''
Draws all food in activeFood
'''


def drawFood():
    for food in activeFood:
        screen.blit(food.image, (food.pos_x, food.pos_y))


'''
if food was picked up, food is removed and lifespan is increased
otherwise identifies the nearest food

'''


def checkFoodPickUp():
    for ant in ant_group:
        shortestDistance = 10000
        closestFood = 0
        for food in activeFood:
            if p.Rect.collidepoint(food.rect, ant.pos_x, ant.pos_y):
                activeFood.remove(food)
                ant.image = IMAGES["A1"]
                ant.lifespan += FOOD_PICK_UP_LIFESPAN_INCREASE
            distance = ((food.pos_x - ant.pos_x)**2 +
                        (food.pos_y - ant.pos_y)**2)**(1/2)
            if distance.real < shortestDistance:
                shortestDistance = distance.real
                closestFood = food

        ant.closestFood = closestFood
        ant.distance = shortestDistance

# Creates offspring randomly located around parent


def offspring(ant):
    for i in range(NUMBER_OF_OFFSPRING):
        i = Ant("A3", ant.pos_x + random.randint(-5, 5),
                ant.pos_y+random.randint(-5, 5))
        ant_group.add(i)


def main():

    loadImages()
    setup(NUMBER_OF_ANTS_AT_START, NUMBER_OF_FOOD_AT_START)

    while True:
        screen.fill("black")

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()

        checkFoodPickUp()
        chanceOfFood(FOOD_PER_TICK)
        drawFood()

        for ant in ant_group:  # move and draw ants
            ant.lifespan -= 1
            ant.age += 1
            if ant.lifespan == 0:
                ant_group.remove(ant)
            if ant.age > MATURITY and ant.image == IMAGES["A3"]:
                ant.image = IMAGES["A2"]
            if len(ant_group) * len(activeFood) < MAX_ENTITIES:
                if len(ant_group) < MAX_ANTS:
                    if ant.lifespan == ENERGY_REQUIREMENT_TO_REPRODUCE:
                        offspring(ant)
            ant.move()
            screen.blit(ant.image, (ant.pos_x, ant.pos_y))

        p.display.flip()
        # time.sleep(.1)
        clock.tick(FPS)


if __name__ == "__main__":
    main()
