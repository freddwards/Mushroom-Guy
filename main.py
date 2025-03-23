import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import os
import csv
import math

from vector import Vector
from player import Player
from level import Level
from level import Block
import constants
from player import Health




class Game:
    def __init__(self):
        self.running = True
        self.state = 1
        self.level = 1
        self.right = False
        self.left = False
        self.jump = False
        self.blocks = []
        self.moss = []

        # Define world data
        self.world_data = world_data = []
        self.loadLevel()
        self.screen_scroll = [0, 0]

        self.tile_list = []
        self.loadImages()

        # Declare player
        self.player = Player(Vector(200, 150))
        self.interaction = Interaction(self)
        # Declare level
        self.level = Level()
        # Process level data
        self.level.process_data(self.world_data, self.tile_list)

    def draw(self, canvas):
        self.level.update(self.screen_scroll)
        self.level.draw(canvas)
        self.player.draw(canvas)
        self.update()
        for block in self.blocks:
            block.draw(canvas)

    def update(self):
        # Call move method for player based on player inputs
        self.screen_scroll = self.player.move(self.left, self.right, self.jump) # takes output for moving screen
        self.interaction.check_and_handle_collisions()

    def keyDown(self, key):  # Handle key presses
        if key == simplegui.KEY_MAP['d']:
            self.right = True
        elif key == simplegui.KEY_MAP['a']:
            self.left = True
        elif key == simplegui.KEY_MAP['space']:
            self.jump = True

    def keyUp(self, key):  # Handle key releases
        if key == simplegui.KEY_MAP['d']:
            self.right = False
        elif key == simplegui.KEY_MAP['a']:
            self.left = False
        elif key == simplegui.KEY_MAP['space']:
            self.jump = False

    def loadImages(self):
        # Load tilemap images
        for x in range(constants.TILE_TYPES):
            absolute_path = os.path.abspath(f"assets/tiles/{x}.png")
            image = simplegui.load_image(absolute_path)
            self.tile_list.append(image)

    def loadLevel(self):
        for row in range(150): # creating empty 150x150 world_data list
            r = [-1] * 150
            self.world_data.append(r)
        #loading level data from csv file into world_data
        with open("levels/level0_data.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    self.world_data[x][y] = int(tile)


class Interaction:
    def __init__(self, game):
        self.game = game


    def check_and_handle_collisions(self):
        self.handle_tile_collisions()  # tile collisions
        # self.handle_moss_collisions()


    # def handle_moss_collisions(self):
    #    for moss in self.game.moss:
    #        if moss.is_player_on_moss(self.game.player):
    #            self.game.player.on_moss = True

    def handle_tile_collisions(self):
        self.game.player.on_ground = False  # assume the player is not on the tile

        for tile in self.game.level.map_tiles:
            if self.is_colliding_with_tile(self.game.player, tile):
                self.resolve_tile_collision(self.game.player, tile)

                if self.game.player.is_on_tile(tile):
                    self.game.player.on_ground = True  # player is on top of the tile

    def is_colliding_with_tile(self, player, tile):
        player_left = player.pos.x - player.size[0] / 2
        player_right = player.pos.x + player.size[0] / 2
        player_top = player.pos.y - player.size[1] / 2
        player_bottom = player.pos.y + player.size[1] / 2

        self.tile_left = tile[1]  - constants.TILE_SIZE / 2 # tile[1] is the x-coordinate of the tile
        self.tile_right = tile[1] + constants.TILE_SIZE / 2
        self.tile_top = tile[2] -  constants.TILE_SIZE / 2  # tile[2] is the y-coordinate of the tile
        self.tile_bottom = tile[2] + constants.TILE_SIZE / 2

        return (player_right > self.tile_left and player_left < self.tile_right and
                player_bottom > self.tile_top and player_top < self.tile_bottom)


    def resolve_tile_collision(self, player, tile):
        overlap_x = min(
            abs(player.pos.x + player.size[0] / 2 - tile[1]),
            abs(player.pos.x - player.size[0] / 2 - (tile[1] + constants.TILE_SIZE))
        )

        overlap_y = min(
            abs(player.pos.y + player.size[1] / 2 - tile[2]),
            abs(player.pos.y - player.size[1] / 2 - (tile[2] + constants.TILE_SIZE))
        )

        if overlap_x < overlap_y:
            # horizontal collision
            if player.pos.x < self.tile_left:
                player.pos.x = self.tile_left - player.size[0] / 2
            elif player.pos.x > self.tile_right:
                player.pos.x = self.tile_right + player.size[0] / 2
            player.vel.x = 0
        else:
            # vertical collision
            if player.pos.y < self.tile_top:
                player.pos.y = self.tile_top - player.size[1] / 2
                player.on_ground = True


            else:
                player.pos.y = self.tile_top + constants.TILE_SIZE + player.size[1] / 2
                player.vel.y = 0

    def is_on_tile(self, player, tile):
        player_bottom = player.pos.y + player.size[1] / 2

        if abs(player_bottom - self.tile_top) < 5:  # tolerance for inaccuracies
            player_left = player.pos.x - player.size[0] / 2
            player_right = player.pos.x + player.size[0] / 2
            tile_left = tile[1]
            tile_right = tile[1] + constants.TILE_SIZE

            if player_right > tile_left and player_left < tile_right:
                return True

        return False


# Create frame and start game
frame = simplegui.create_frame("Mushroom Guy", constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
game = Game()
frame.set_draw_handler(game.draw)
frame.set_keydown_handler(game.keyDown)
frame.set_keyup_handler(game.keyUp)
frame.start()
