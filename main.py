import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import os
import csv

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

        # declaring player object
        self.player = Player(Vector(200, 150))

        # declaring several moss objects
        self.moss = [
            # position (x, y) , height , width
            Moss(Vector(200, 600), 10, 200),
            Moss(Vector(50, 600), 10, 100),
            Moss(Vector(500, 600), 10, 50)
        ]

        # Initialize tile_list and world_data
        self.tile_list = []
        self.world_data = []

        # Initialize screen_scroll
        self.screen_scroll = 0

        # Load images and level data
        self.loadImages()
        self.loadLevel()

    def draw(self, canvas):
        self.player.draw(canvas)

        # drawing the moss objects
        for moss in self.moss:
            moss.draw(canvas)

        self.update()

    def update(self):
        # call move method for player based on player inputs
        self.screen_scroll = self.player.move(self.left, self.right, self.jump)  # takes output for moving screen

        # checking if the player is in contact with the moss
        on_moss = False
        for moss in self.moss:
            if moss.is_player_on_moss(self.player):
                on_moss = True
                break

        if on_moss:
            self.player.vel.x *= constants.SLOW_FACTOR  # Reduce horizontal velocity
            self.player.vel.y *= constants.SLOW_FACTOR  # Reduce vertical velocity (optional)

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

    def loadImages(self):
        # Load tilemap images
        for x in range(constants.TILE_TYPES):
            absolute_path = os.path.abspath(f"assets/tiles/{x}.png")
            image = simplegui.load_image(absolute_path)
            self.tile_list.append(image)

    def loadLevel(self):
        for row in range(150):  # creating empty 150x150 world_data list
            r = [-1] * 150
            self.world_data.append(r)
        # loading level data from csv file into world_data
        with open("levels/level0_data.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    self.world_data[x][y] = int(tile)


frame = simplegui.create_frame("Mushroom Guy", constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
game = Game()
frame.set_draw_handler(game.draw)
frame.set_keydown_handler(game.keyDown)
frame.set_keyup_handler(game.keyUp)

frame.start()
