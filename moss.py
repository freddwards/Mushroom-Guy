import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
import math

# Constants
# WINDOW_WIDTH = 400
# WINDOW_HEIGHT = 400

class Moss:
    def __init__(self,pos,height,width):
        # we need to get the x, y, height, width
        self.pos = pos
        self.height = height
        self.width = width



    def draw(self, canvas):
        # using a line is not working so im going to use a polygon
        canvas.draw_polygon([(self.pos.x, self.pos.y ),
                            ( self.pos.x +self.width ,self.pos.y),
                            (self.pos.x + self.width, self.pos.y-self.height),
                            (self.pos.x , self.pos.y-self.height)], 1,"Green","Green")


        # Draw a rectangle representing the moss
        #canvas.draw_line((self.start.x,self.start.y),(self.end.x,self.end.y),25,"Green")

    # function to figure out if the player is touching the moss
    def is_player_on_moss (self,player):
        # checking is the player is near the moss
        # get the player position
        player_bottom = player.pos.y +player.size[1] /2
        player_left = player.pos.x - player.size[0]/2
        player_right = player.pos.x + player.size [0] / 2

        moss_top = self.pos.y
        moss_left = self.pos.x
        moss_right = self.pos.x +self.width

        # Check if the player is exactly on top of the moss
        if moss_left < player_right and player_left < moss_right:  # Player is horizontally over the moss
            if abs(player_bottom - moss_top) < 5 and player.vel.y >= 0:  # Close enough to land & falling
                return True
        return False





