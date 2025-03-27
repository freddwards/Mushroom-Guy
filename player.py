import constants
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from constants import SCROLL_THRESH_Y
from vector import Vector
from level import Level

class Health:
    def __init__(self, max_health, game):
        self.game = game
        self.max_health = constants.LIVES
        self.current_health = max_health

        # Load heart image directly in the Health class
        self.heart_image = simplegui.load_image(constants.HEART_IMAGE_URL)

    def life_lost(self):
        # Current health decreases by 1
        if self.current_health > 0:
            self.current_health -= 1
    
    def life_gained(self, amount):
        # current health increases by {amount}
        if self.current_health + amount <= self.max_health:
            self.current_health += amount
        else:
            self.current_health = self.max_health

    def reset(self):
        self.current_health = self.max_health

    def draw(self, canvas):
        if self.heart_image.get_width() > 0:  # Right now the heart lives dont load
            for i in range(self.current_health):
                x = constants.SCREEN_WIDTH - (constants.HEART_IMAGE_SIZE[0] + constants.HEART_IMAGE_SPACING) * (i + 1)
                y = constants.HEART_IMAGE_SPACING + constants.HEART_IMAGE_SIZE[1] / 2
                canvas.draw_image(self.heart_image,
                                  (self.heart_image.get_width() / 2, self.heart_image.get_height() / 2),
                                  (self.heart_image.get_width(), self.heart_image.get_height()),
                                  (x, y),
                                  constants.HEART_IMAGE_SIZE)
                
class Player:
    def __init__(self, pos, game):
        self.game = game
        self.pos = pos
        self.size = (constants.TILE_SIZE, constants.TILE_SIZE)  # Size of the character (width and height) same as tile for consistancy
        self.speed = constants.PLAYER_SPEED
        self.on_ground = False
        self.vel = Vector(0, 0)
        self.on_block = False
        self.health = Health(constants.LIVES, self.game)  # Initialize health with 3 hearts
        self.gravity = constants.GRAVITY
        self.speed_time = 0
        self.gravity_time = 0
        self.checkpoint = Vector(0, 0)
        self.uptime = 0

    def draw(self, canvas):

        # update the status of the powerups
        self.update_powerups()

        # Draw a rectangle representing the character
        canvas.draw_polygon([
            # drawing a polygon with the character's position and size
            (self.pos.x - self.size[0] / 2, self.pos.y - self.size[1] / 2),
            (self.pos.x + self.size[0] / 2, self.pos.y - self.size[1] / 2),
            (self.pos.x + self.size[0] / 2, self.pos.y + self.size[1] / 2),
            (self.pos.x - self.size[0] / 2, self.pos.y + self.size[1] / 2)
        ], 1, "Black", "Red")

        # Draws the player's health
        self.health.draw(canvas)

        self.uptime += 1
    
    def return_to_checkpoint(self):
        self.game.return_to_checkpoint()
        self.uptime = 0

    def collect_powerup(self, type):
        if type == "health":
            self.health.life_gained(1)
        elif type == "speed":
            self.speed_time += 600
        elif type == "gravity":
            self.gravity_time += 600
        elif type == "damage":
            print("lava")
            self.health.life_lost()
            self.return_to_checkpoint()
        elif type == "ladder":
            if self.game.current_level <3:
                self.game.current_level += 1
                self.return_to_checkpoint()

    def update_powerups(self):
        if self.speed_time > 0:
            self.speed_time -= 1
            self.speed = constants.PLAYER_SPEED * 1.2
            if self.speed_time == 0:
                self.speed = constants.PLAYER_SPEED
        if self.gravity_time > 0:
            self.gravity_time -= 1
            self.gravity = constants.GRAVITY * 0.8
            if self.gravity_time == 0:
                self.gravity = constants.GRAVITY

    def move(self, left, right, jump):
        screen_scroll = [0, 0]

        if (self.on_ground) == False:
            self.vel.y += self.gravity
        elif jump and (self.on_ground):  # only when on ground can character jump
            self.vel.y = constants.JUMP_POWER
        else:
            self.vel.y = 0

        if self.vel.y > constants.TERMINAL_VELOCITY:
            self.vel.y = constants.TERMINAL_VELOCITY

        if self.uptime >= 60:
            self.pos.add(self.vel)

        # updating character x coords based on player inputs
        vel_x = 0
        if right:
            vel_x = self.speed
        if left:
            vel_x = -self.speed
        self.vel.x = vel_x


        # adjusting screen scroll based on players position
        if self.pos.x > (constants.SCREEN_WIDTH - constants.SCROLL_THRESH_X): # check right side
            screen_scroll[0] = (constants.SCREEN_WIDTH - constants.SCROLL_THRESH_X) - self.pos.x
            self.pos.x = constants.SCREEN_WIDTH - constants.SCROLL_THRESH_X # stop player moving when near right edge
            
        if self.pos.x < constants.SCROLL_THRESH_X: # check left side
            screen_scroll[0] = constants.SCROLL_THRESH_X - self.pos.x
            self.pos.x = constants.SCROLL_THRESH_X # stop player movinf when near left edge
            
        if self.pos.y > (constants.SCREEN_HEIGHT - SCROLL_THRESH_Y):  # check bottom 
            screen_scroll[1] = (constants.SCREEN_HEIGHT - SCROLL_THRESH_Y) - self.pos.y
            self.pos.y = constants.SCREEN_HEIGHT - SCROLL_THRESH_Y  # stop player moving when near bottom
            
        if self.pos.y < constants.SCROLL_THRESH_Y:  # check top
            screen_scroll[1] = constants.SCROLL_THRESH_Y - self.pos.y
            self.pos.y = constants.SCROLL_THRESH_Y  # stop player moving when near top

        return screen_scroll

    def is_on_tile(self, tile):
        # players bottom edge
        player_bottom = self.pos.y + self.size[1] / 2
        # tiles top edge
        tile_top = tile[2]

        # check if the players bottom is close to the tiles top
        if abs(player_bottom - tile_top) < 5: # tolerance for inaccuracies
            player_left = self.pos.x - self.size[0] / 2
            player_right = self.pos.x + self.size[0] / 2
            tile_left = tile[1]
            tile_right = tile[1] + constants.TILE_SIZE

            if player_right > tile_left and player_left < tile_right:
                return True
        return False

    def reset_speed(self):
        # reset the player's speed to the default value
        self.speed = self.default_speed
