import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import os
import csv
import math
import time

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
        self.tile_list = []
        
        # get the absolute path and convert to proper format (fix for images not loading)
        base_dir = os.path.abspath("assets/tiles")
        base_uri = f"file:///{base_dir.replace('\\', '/')}"
        
        for x in range(constants.TILE_TYPES):

            img_uri = f"{base_uri}/{x}.png"
            print(f"Loading image: {img_uri}")
            
            # load the image
            img = simplegui.load_image(img_uri)
            
            # check if the image loaded properly
            if img.get_width() == 0:
                print(f"Image {x}.png didn't load properly - using placeholder")
                # create a placeholder blank image
                img = simplegui._create_blank_image(constants.TILE_SIZE, constants.TILE_SIZE)
                img.fill((255, 255, 255))  # white placeholder
            
            self.tile_list.append(img)
            print(f"Loaded tile {x} - Dimensions: {img.get_width()}x{img.get_height()}")

    def loadLevel(self):
        for row in range(150): # creating empty 150x150 world_data list
            r = [-1] * 150
            self.world_data.append(r)
        # loading level data from csv file into world_data
        with open("levels/level0_data.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    self.world_data[x][y] = int(tile)


class Interaction:
    def __init__(self, game):
        self.game = game
        self.collision_tolerance = 0.1  # small threshold to prevent jittering

    def check_and_handle_collisions(self):
        self.handle_tile_collisions()

    def handle_tile_collisions(self):
        self.game.player.on_ground = False
        
        for tile in self.game.level.map_tiles:
            if self.is_colliding_with_tile(self.game.player, tile):
                self.resolve_tile_collision(self.game.player, tile)
                self.check_on_ground(self.game.player, tile)

    def is_colliding_with_tile(self, player, tile):
        # find player bounds
        player_left = player.pos.x - player.size[0]/2
        player_right = player.pos.x + player.size[0]/2
        player_top = player.pos.y - player.size[1]/2
        player_bottom = player.pos.y + player.size[1]/2

        # find tile bounds
        tile_left = tile[1] - constants.TILE_SIZE/2
        tile_right = tile[1] + constants.TILE_SIZE/2
        tile_top = tile[2] - constants.TILE_SIZE/2
        tile_bottom = tile[2] + constants.TILE_SIZE/2

        return (player_right > tile_left and 
                player_left < tile_right and 
                player_bottom > tile_top and 
                player_top < tile_bottom)

    def resolve_tile_collision(self, player, tile):
        # find bounds with threshold
        tile_left = tile[1] - constants.TILE_SIZE/2 + self.collision_tolerance
        tile_right = tile[1] + constants.TILE_SIZE/2 - self.collision_tolerance
        tile_top = tile[2] - constants.TILE_SIZE/2 + self.collision_tolerance
        tile_bottom = tile[2] + constants.TILE_SIZE/2 - self.collision_tolerance

        # find penetration distances
        penetration_left = (player.pos.x + player.size[0]/2) - tile_left
        penetration_right = tile_right - (player.pos.x - player.size[0]/2)
        penetration_top = (player.pos.y + player.size[1]/2) - tile_top
        penetration_bottom = tile_bottom - (player.pos.y - player.size[1]/2)

        # find smallest penetration
        min_penetration = min(penetration_left, penetration_right, 
                             penetration_top, penetration_bottom)

        # resolve collision based on smallest penetration
        if min_penetration == penetration_left:
            # collision from left side
            player.pos.x = tile_left - player.size[0]/2 - self.collision_tolerance
            player.vel.x = 0
            
        elif min_penetration == penetration_right:
            # collision from right side
            player.pos.x = tile_right + player.size[0]/2 + self.collision_tolerance
            player.vel.x = 0
            
        elif min_penetration == penetration_top:
            # collision from top
            player.pos.y = tile_top - player.size[1]/2 - self.collision_tolerance
            player.vel.y = 0
            
        else:  # penetration_bottom
            # collision from bottom
            player.pos.y = tile_bottom + player.size[1]/2 + self.collision_tolerance
            player.vel.y = 0

    def check_on_ground(self, player, tile):
        # check if the player is on the ground
        player_bottom = player.pos.y + player.size[1]/2
        tile_top = tile[2] - constants.TILE_SIZE/2
        
        if (abs(player_bottom - tile_top) < 5 and  # Small tolerance
            player.pos.x + player.size[0]/2 > tile[1] - constants.TILE_SIZE/2 and
            player.pos.x - player.size[0]/2 < tile[1] + constants.TILE_SIZE/2):
            player.on_ground = True

# Create frame and start game
frame = simplegui.create_frame("Mushroom Guy", constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
game = Game()
frame.set_draw_handler(game.draw)
frame.set_keydown_handler(game.keyDown)
frame.set_keyup_handler(game.keyUp)
frame.start()
