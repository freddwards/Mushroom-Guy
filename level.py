import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import constants


class Level():
    def __init__(self):
        self.map_tiles = []

    def process_data(self,data,tile_list):
        self.level_length = len(data)
        # go through every value in data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile < 0:
                    continue
                image = tile_list[tile]
                image_width = image.get_width()
                image_height = image.get_height()
                image_x = x * constants.TILE_SIZE
                image_y = y * constants.TILE_SIZE
                tile_data = [image, image_x, image_y]

                #add the image data to the tiles list
                if tile >=0: # helps to create empty space
                    self.map_tiles.append(tile_data)

    def update(self, screen_scroll):
        for tile in self.map_tiles:
            tile[1] += screen_scroll[0] # move tile x coord based on screen scroll
            tile[2] += screen_scroll[1] # move tiles y coord based on screen scroll
            

    def draw(self, canvas):
        for tile in self.map_tiles:
            image = tile[0]
            position = (tile[1], tile[2])

            canvas.draw_image(
                image,
                (image.get_width() // 2, image.get_height() // 2),  # Source center
                (image.get_width(), image.get_height()),  # Source size
                position, 
                (constants.TILE_SIZE, constants.TILE_SIZE))  # Drawn size

class Block:
    def __init__(self, center, color="red"):

        self.center = center
        self.size = (constants.TILE_SIZE, constants.TILE_SIZE)
        self.color = color

    def draw(self, canvas):

        # calculate the top-left corner of the block
        top_left = (self.center[0] - self.size[0] / 2, self.center[1] - self.size[1] / 2)
        # calculate the four corners of the block
        points = [
            top_left,
            (top_left[0] + self.size[0],  top_left[1]),
            (top_left[0] + self.size[0], top_left[1] + self.size[1]),
            (top_left[0], top_left[1] + self.size[1])
        ]
        # draw the block
        canvas.draw_polygon(points, 1, self.color, self.color)
