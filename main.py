import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import Vector
from player import Player
import constants


class Game:
    def __init__(self):
        self.running = True
        self.state = 1
        self.level = 1
        self.right = False
        self.left = False
        self.jump = False

        # declaring player object
        self.player = Player(Vector(200, 150))

    def draw(self, canvas):
        self.player.draw(canvas)
        self.update()

    def update(self):
        # call move method for player based on player inputs
        self.player.move(self.left, self.right, self.jump)

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


frame = simplegui.create_frame("Mushroom Guy", constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
game = Game()
frame.set_draw_handler(game.draw)
frame.set_keydown_handler(game.keyDown)
frame.set_keyup_handler(game.keyUp)

frame.start()
