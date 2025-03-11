import constants
import csv


class Level:
    def __init__(self):
        self.level_length = None
        self.map_tiles = []
        self.collision_tiles = []
        self.exit_tile = None

    def process_data(self, data, tile_list, mob_animations):
        self.level_length = len(data)
        # iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x * constants.TILE_SIZE
                image_y = y * constants.TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]

                # checks for special tiles and spawns in what they represents
                if tile == 7:
                    self.collision_tiles.append(tile_data)
                # elif tile == 8:
                #    self.exit_tile = tile_data

                # add image data to main tiles list
                if tile >= 0:
                    self.map_tiles.append(tile_data)

    def update(self, screen_scroll):
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]  # moving tiles based on screen scroll
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])


def import_tiles(current_level):
    # create empty tile list
    level_data = []
    for row in range(constants.ROWS):
        r = [-1] * constants.COLS
        level_data.append(r)
    # load in world data and create a level
    with open(f"levels/level{current_level - 1}_data.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")  # coma defines when next tile starts
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                level_data[x][y] = int(tile)
    return level_data

# resetting level when needed only have 1 lvl for now
# def reset_level():


# create empty tile list
# data = []
# for row in range(constants.ROWS):
#    r = [-1] * constants.COLS
#    data.append(r)
# return data
