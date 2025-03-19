import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import constants

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