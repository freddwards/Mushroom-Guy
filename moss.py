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
        if (self.pos.x<player.pos.x< self.pos.x+self.width):
            if (self.pos.y - self.height <=  player.pos.y + player.size // 2 <= self.pos.y):
                return True
        return False


