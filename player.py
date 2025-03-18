import constants
from vector import Vector

FLOOR = constants.SCREEN_HEIGHT - 11  # temp before map is added

class Health:
    def __init__(self, max_health):
        self.max_health = constants.LIVES
        self.current_health = max_health

        #Load heart image directly in the Health class
        self.heart_image = simplegui.load_image(constants.HEART_IMAGE_URL)

    def life_lost(self):
        #Current health decreases by 1
        if self.current_health > 0:
            self.current_health -= 1
    
    def reset(self):
        self.current_health = self.max_health

    def draw(self, canvas):
        if self.heart_image.get_width() > 0:  #Right now the heart lives dont load
            for i in range(self.current_health):
                x = constants.SCREEN_WIDTH - (constants.HEART_IMAGE_SIZE[0] + constants.HEART_IMAGE_SPACING) * (i + 1)
                y = constants.HEART_IMAGE_SPACING + constants.HEART_IMAGE_SIZE[1] / 2
                canvas.draw_image(self.heart_image, 
                                 (self.heart_image.get_width() / 2, self.heart_image.get_height() / 2),
                                 (self.heart_image.get_width(), self.heart_image.get_height()),
                                 (x, y),
                                 constants.HEART_IMAGE_SIZE)
        else:
            #Image doesnt work so for now lives are rectangles
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
        self.size = constants.TILE_SIZE  # Size of the character (width and height) same as tile for consistency
        self.speed = constants.PLAYER_SPEED  # current speed
        self.on_ground = False
        self.vel = Vector(0, 0)
        self.default_speed = constants.DEFAULT_PLAYER_SPEED  # Save default speed
        self.health = Health(constants.LIVES)    # Initialize health with 3 hearts

    def draw(self, canvas):
        # Draw a rectangle representing the character
        canvas.draw_polygon([
            # drawing a polygon with the character's position and size
            (self.pos.x - self.size / 2, self.pos.y - self.size / 2),
            (self.pos.x + self.size / 2, self.pos.y - self.size / 2),
            (self.pos.x + self.size / 2, self.pos.y + self.size / 2),
            (self.pos.x - self.size / 2, self.pos.y + self.size / 2)
        ], 1, "Black", "Red")

        #Draws the player's health
        self.health.draw(canvas)

    def move(self, left, right, jump):
        screen_scroll = [0, 0]
        self.vel.y += constants.GRAVITY
        self.pos.add(self.vel)

        # preventing character from falling forever
        if self.pos.y >= FLOOR:
            self.pos.y = FLOOR
            # check if character is on the ground
            self.on_ground = True
        else:
            self.on_ground = False

        # updating character x coords based on player inputs
        vel_x = 0
        if right:
            vel_x = constants.PLAYER_SPEED
        if left:
            vel_x = -constants.PLAYER_SPEED
        self.vel.x = vel_x

        if jump and self.on_ground:  # only when on ground can character jump
            self.vel.y = constants.JUMP_POWER

        # adjusting screen scroll based on player's position
        if self.pos.x > (constants.SCREEN_WIDTH - constants.SCROLL_THRESH):  # check right side
            screen_scroll[0] = (constants.SCREEN_WIDTH - constants.SCROLL_THRESH) - self.pos.x
            self.pos.x = constants.SCREEN_WIDTH - constants.SCROLL_THRESH  # stop player moving when near right edge

        if self.pos.x < constants.SCROLL_THRESH:  # check left side
            screen_scroll[0] = constants.SCROLL_THRESH - self.pos.x
            self.pos.x = constants.SCROLL_THRESH  # stop player moving when near left edge

        # if self.pos.y > (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH):  # check bottom # temp removed to stop player endless falling
        #     screen_scroll[1] = (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH) - self.pos.y
        #     self.pos.y = constants.SCREEN_HEIGHT - constants.SCROLL_THRESH  # stop player moving when near bottom

        if self.pos.y < constants.SCROLL_THRESH:  # check top
            screen_scroll[1] = constants.SCROLL_THRESH - self.pos.y
            self.pos.y = constants.SCROLL_THRESH  # stop player moving when near top

        return screen_scroll

    def reset_speed(self):
        # Reset the player's speed to the default value
        self.speed = self.default_speed


# Example usage
player = Player(Vector(100, 100))
