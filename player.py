import constants
from vector import Vector

FLOOR = constants.SCREEN_HEIGHT - 11  # temp before map is added


class Player:
    def __init__(self, pos):
        self.pos = pos
        self.size = 22  # Size of the character (width and height)
        self.speed = constants.PLAYER_SPEED # current speed
        self.on_ground = False
        self.vel = Vector(0, 0)

        self.default_speed = constants.DEFAULT_PLAYER_SPEED  # Save default speed


    def draw(self, canvas):
        # Draw a rectangle representing the character
        canvas.draw_polygon([
            # drawing a polygon with the character's position and size
            (self.pos.x - self.size / 2, self.pos.y - self.size / 2),
            (self.pos.x + self.size / 2, self.pos.y - self.size / 2),
            (self.pos.x + self.size / 2, self.pos.y + self.size / 2),
            (self.pos.x - self.size / 2, self.pos.y + self.size / 2)
        ], 1, "Black", "Red")

    def move(self, left, right, jump):
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

    def reset_speed(self, speed):
        # Reset the player's speed to the default value
        self.speed = self.default_speed
        #self.jump_power = self.default_jump






# Example usage
player = Player(Vector(100, 100))
