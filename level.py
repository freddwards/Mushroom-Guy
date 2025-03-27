import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import constants


class Level():
    def __init__(self, game):
        self.game = game
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
        for powerup in self.game.powerups:
            powerup.pos.x += screen_scroll[0]
            powerup.pos.y += screen_scroll[1]
            

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

class Powerup:
    def __init__(self, game, pos, type):
        self.pos = pos
        self.game = game
        self.size = (constants.TILE_SIZE, constants.TILE_SIZE)
        if type == 0:
            self.type = "health"
            self.img = game.powerup_images[0]
        elif type == 1:
            self.type = "speed"
            self.img = game.powerup_images[1]
        elif type == 2:
            self.type = "gravity"
            self.img = game.powerup_images[2]
        elif type == 3:
            self.type = "damage"
            self.img = game.tile_list[20]
        elif type == 4:
            self.type = "ladder"
            self.img = game.tile_list[22]
        

    def draw(self, canvas):
        canvas.draw_image(self.img,(self.img.get_width() // 2, self.img.get_height() // 2),  (self.img.get_width(), self.img.get_height()), (self.pos.x,self.pos.y), (constants.TILE_SIZE, constants.TILE_SIZE))
    
    def collect(self):
        if self.type == "health":
            self.game.player.health.add_health(1)
        elif self.type == "speed":
            self.game.player.collect_powerup("speed")
        elif self.type == "gravity":
            self.game.player.collect_powerup("gravity")
        elif self.type == "damage":
            self.game.player.collect_powerup("damage")
        elif self.type == "ladder":
            self.game.player.collect_powerup("ladder")
        self.game.powerups.remove(self)