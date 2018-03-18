import random

import pygame as pg

"""
from numpy.random import choice as npchoice
use method=npchoice([0, 1], p=[0.8, 0.2]) to generate walls that are 4x more likely to be open than walls
"""
random.seed(1)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BROWN = (139, 69, 19)

WIDTH = 800
HEIGHT = 600
TILE_SIZE = 25
WALL_WIDTH = 2
CIRCLE_RADIUS = 10
WORLD_X = 15
WORLD_Y = 15
START_X = 7
START_Y = 7

HEALTH = 3
ITEMS = ["Sword", "Potion", "Trapdoor", "Stairs", "Book", "Scroll", "NPC"]


def wall_gen_uniform():
    while True:
        yield random.randint(0,1)


class Tile(pg.sprite.Sprite):

    def __init__(self, origin, walls=False, add_items=False):
        super().__init__()
        self.background_color = WHITE
        self.neighbors = []
        self.origin = origin
        self.tile_dimension = TILE_SIZE
        self.show_walls = walls
        self.walls = {"up": None, "down": None, "left": None, "right": None}
        self.contents = []
        if add_items:
            for item in ITEMS:
                a = random.random()
                if a < 0.05:
                    self.contents.append(item)


    def add_walls(self, g, x, y, method=wall_gen_uniform()):
        # check if tile left exists, if so if there is a shared wall
        if x == 0:  # edge of world
            self.walls["left"] = 1
        elif g.grid[x-1][y] is None:  # unexplored
            self.walls["left"] = next(method)
        else:  # take over existing tile's right wall value
            self.walls["left"] = g.grid[x-1][y].walls["right"]
        # check if tile right exists, if so if there is a shared wall
        if x == WORLD_X-1:
            self.walls["right"] = 1
        elif g.grid[x+1][y] is None:
            self.walls["right"] = next(method)
        else:
            self.walls["right"] = g.grid[x + 1][y].walls["left"]
        # check if tile up exists, if so if there is a shared wall
        if y == 0:
            self.walls["up"] = 1
        elif g.grid[x][y-1] is None:
            self.walls["up"] = next(method)
        else:
            self.walls["up"] = g.grid[x][y-1].walls["down"]
        # check if tile down exists, if so if there is a shared wall
        if y == WORLD_Y-1:
            self.walls["down"] = 1
        elif g.grid[x][y+1] is None:
            self.walls["down"] = next(method)
        else:
            self.walls["down"] = g.grid[x][y+1].walls["up"]

    def draw(self, surface):
        if self.show_walls:
            dims = [self.origin[0]+WALL_WIDTH/2,
                    self.origin[1]+WALL_WIDTH/2,
                    self.tile_dimension-WALL_WIDTH,
                    self.tile_dimension-WALL_WIDTH]
            if self.walls["up"] == 1:
                pg.draw.rect(surface, RED, [self.origin[0],
                                              self.origin[1],
                                              self.tile_dimension,
                                              WALL_WIDTH/2])
            if self.walls["right"] == 1:
                pg.draw.rect(surface, RED, [self.origin[0]+self.tile_dimension,
                                              self.origin[1],
                                              -WALL_WIDTH / 2,
                                              self.tile_dimension])
            if self.walls["down"] == 1:
                pg.draw.rect(surface, RED, [self.origin[0],
                                              self.origin[1]+self.tile_dimension,
                                              self.tile_dimension,
                                              -WALL_WIDTH/2])
            if self.walls["left"] == 1:
                pg.draw.rect(surface, RED, [self.origin[0],
                                              self.origin[1],
                                              WALL_WIDTH / 2,
                                              self.tile_dimension])
        else:
            dims = [self.origin[0],
                    self.origin[1],
                    self.tile_dimension,
                    self.tile_dimension]
        pg.draw.rect(surface, self.background_color, dims)


class Grid:

    def __init__(self, x_size, y_size):
        self.grid = [[None for _ in range(x_size)] for _ in range(y_size)]

    def add_tile(self, Tile, x, y):
        if self.grid[x][y] is None:
            self.grid[x][y] = Tile
        else:
            print("tile already at this location")

    def is_occupied(self, x, y):
        return self.grid[x][y] is not None


def main(with_walls=True):
    pg.init()
    ticks = 0
    size = (WIDTH, HEIGHT)
    screen = pg.display.set_mode(size)
    clock = pg.time.Clock()
    font = pg.font.SysFont('Arial', 18)
    done = False
    world = Grid(WORLD_X, WORLD_Y)
    circle_x = WIDTH/2
    circle_y = HEIGHT/2
    tiles_list = []
    init_tile = Tile([WIDTH/2 - TILE_SIZE/2, HEIGHT/2 - TILE_SIZE/2], walls=with_walls, add_items=False)
    init_tile.add_walls(world, START_X, START_Y)
    tiles_list.append(init_tile)
    world.add_tile(init_tile, START_X, START_Y)
    grid_loc = [START_X, START_Y]
    current_tile = init_tile

    while not done:
        screen.fill(BLACK)
        circle_moved = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    if current_tile.walls["left"]:
                        print("hit a wall, can't move left)")
                    else:
                        circle_x -= TILE_SIZE
                        circle_moved = True
                        grid_loc[0] -= 1
                        print("moving left")
                elif event.key == pg.K_RIGHT:
                    if current_tile.walls["right"]:
                        print("hit a wall, can't move right)")
                    else:
                        circle_x += TILE_SIZE
                        circle_moved = True
                        grid_loc[0] += 1
                        print("moving right")
                elif event.key == pg.K_UP:
                    if current_tile.walls["up"]:
                        print("hit a wall, can't move up)")
                    else:
                        circle_y -= TILE_SIZE
                        circle_moved = True
                        grid_loc[1] -= 1
                        print("moving up")
                elif event.key == pg.K_DOWN:
                    if current_tile.walls["down"]:
                        print("hit a wall, can't move down)")
                    else:
                        circle_y += TILE_SIZE
                        circle_moved = True
                        grid_loc[1] += 1
                        print("moving down")
                ticks += 1
        if circle_moved:
            # add a check to see if the tile already exists
            if world.is_occupied(grid_loc[0], grid_loc[1]):
                print(f"I've already seen this tile, at {grid_loc[0]}, {grid_loc[1]}")
                # print(world.grid[grid_loc[0]][grid_loc[1]].walls)
                current_tile = world.grid[grid_loc[0]][grid_loc[1]]
            else:
                newtile = Tile([int(circle_x - TILE_SIZE / 2), int(circle_y - TILE_SIZE / 2)], walls=with_walls, add_items=True)
                newtile.add_walls(world, grid_loc[0], grid_loc[1])
                tiles_list.append(newtile)
                world.add_tile(newtile, grid_loc[0], grid_loc[1])
                current_tile = newtile
            print(f"Current tile has {current_tile.contents}")
        for tile in tiles_list:
            tile.draw(screen)
        pg.draw.circle(screen, RED, [int(circle_x), int(circle_y)], CIRCLE_RADIUS)
        textsurf = font.render(f"Steps: {ticks}", False, RED)
        healthsurf = font.render(f"Health: {HEALTH}", False, RED)
        screen.blit(textsurf, (0, 0))
        screen.blit(healthsurf, (WIDTH*0.8, 0))
        pg.display.flip()
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    main(with_walls=True)
