import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from constants import SCREEN_HEIGHT
from vector import Vector
from player import Player
from moss import Moss

import constants

class Game:
    def __init__(self):
        self.running = True
        self.state = 1
        self.level = 1
        self.right = False
        self.left = False
        self.jump = False
        self.damaged_cooldown = 0  # Prevents continuous damage

        # declaring player object
        self.player = Player(Vector(200, 150))

        # declaring several moss objects
        self. moss = [
            # position (x, y) , height , width
             Moss(Vector(200, 600),10,200 ),
             Moss(Vector(50, 600),10,100 ),
             Moss(Vector(500, 600),10 , 50 )
        ]

    def draw(self, canvas):
        self.player.draw(canvas)

        # drawing the moss objects
        for moss in self.moss:
             moss.draw(canvas)

        self.update()

    def update(self):
        # call move method for player based on player inputs
        self.player.move(self.left, self.right, self.jump)

         # checking if the player is in contact with the moss
        on_moss = False
        for moss in self.moss:
            if moss.is_player_on_moss(self.player):
                on_moss = True
                break

        if on_moss:
            self.player.vel.x *= constants.SLOW_FACTOR  # Reduce horizontal velocity
            self.player.vel.y *= constants.SLOW_FACTOR  # Reduce vertical velocity (optional)
            if self.damaged_cooldown == 0:  #Prevents immediate life loss
                self.damaged_player()
                self.damaged_cooldown = 180  #A delay before next damage

        #Decrease cooldown timer
        if self.damaged_cooldown > 0:
            self.damaged_cooldown -= 1

    def keyDown(self, key):  # taking inputs from the player
        if key == simplegui.KEY_MAP['d']:
            self.right = True
        elif key == simplegui.KEY_MAP['a']:
            self.left = True
        elif key == simplegui.KEY_MAP['w']:
            self.jump = True

    def keyUp(self, key):  # ending inputs from the player
        if key == simplegui.KEY_MAP['d']:
            self.right = False
        elif key == simplegui.KEY_MAP['a']:
            self.left = False
        elif key == simplegui.KEY_MAP['w']:
            self.jump = False

    def damaged_player(self):
        self.player.health.life_lost()


frame = simplegui.create_frame("Mushroom Guy", constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
game = Game()
frame.set_draw_handler(game.draw)
frame.set_keydown_handler(game.keyDown)
frame.set_keyup_handler(game.keyUp)
frame.start()
