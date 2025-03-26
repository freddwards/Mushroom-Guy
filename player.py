import constants
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from constants import SCROLL_THRESH_Y
from vector import Vector

FLOOR = constants.SCREEN_HEIGHT - 11  # temp before map is added


class Health:
    def __init__(self, max_health):
        self.max_health = constants.LIVES
        self.current_health = max_health

        # Load heart image directly in the Health class
        self.heart_image = simplegui.load_image(constants.HEART_IMAGE_URL)

    def life_lost(self):
        # Current health decreases by 1
        if self.current_health > 0:
            self.current_health -= 1

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
        else:
            # Image doesnt work so for now lives are rectangles
            for i in range(self.current_health):
                x = constants.SCREEN_WIDTH - (constants.HEART_IMAGE_SIZE[0] + constants.HEART_IMAGE_SPACING) * (i + 1)
                y = constants.HEART_IMAGE_SPACING
                canvas.draw_polygon([
                    (x, y),
                    (x + constants.HEART_IMAGE_SIZE[0], y),
                    (x + constants.HEART_IMAGE_SIZE[0], y + constants.HEART_IMAGE_SIZE[1]),
                    (x, y + constants.HEART_IMAGE_SIZE[1])
                ], 1, "Red", "Red")
                
class Player:
    def __init__(self, pos):
        self.pos = pos
        self.size = (constants.TILE_SIZE, constants.TILE_SIZE)  # Size of the character (width and height) same as tile for consistancy
        self.speed = constants.PLAYER_SPEED
        self.on_ground = False
        self.vel = Vector(0, 0)
        self.on_block = False
        self.health = Health(constants.LIVES)  # Initialize health with 3 hearts

    def draw(self, canvas):
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

    def move(self, left, right, jump):
        screen_scroll = [0, 0]

        if (self.on_ground or self.on_block) == False:
            self.vel.y += constants.GRAVITY
        elif jump and (self.on_ground or self.on_block):  # only when on ground can character jump
            self.vel.y = constants.JUMP_POWER
        else:
            self.vel.y = 0

        # preventing character from falling forever
        if self.pos.y >= FLOOR:
            self.pos.y = FLOOR
            # check if character is on the ground
            self.on_ground = True
        else:
            self.on_ground = False

        if self.vel.y > constants.TERMINAL_VELOCITY:
            self.vel.y = constants.TERMINAL_VELOCITY

        self.pos.add(self.vel)

        # updating character x coords based on player inputs
        vel_x = 0
        if right:
            vel_x = constants.PLAYER_SPEED
        if left:
            vel_x = -constants.PLAYER_SPEED
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
