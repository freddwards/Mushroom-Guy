import simplegui

#Constants
WIDTH = 450
HEIGHT = 300
BAR_WIDTH = 300
BAR_HEIGHT = 30
MAX_HEALTH = 100

#Position the health bar in the top-right corner
BAR_X = WIDTH - BAR_WIDTH  
BAR_Y = 20 

class HealthBar:
    def __init__(self, max_health, x, y, width, height):
        self.max_health = max_health
        self.health = max_health
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def take_damage(self, amount=20):
        #Reduce health and ensure it doesn't go below zero
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def draw(self, canvas):
        canvas.draw_text("Health", (self.x, self.y - 5), 18, "White")

        canvas.draw_polygon([(self.x, self.y), (self.x + self.width, self.y), 
                             (self.x + self.width, self.y + self.height), (self.x, self.y + self.height)], 
                            2, "White", "Black")

        #Calculate bar length based on health
        bar_length = (self.health / self.max_health) * self.width

        #Set bar color based on health
        bar_color = "Green" if self.health > 20 else "Red"

        #Draw actual health bar
        canvas.draw_polygon([(self.x, self.y), (self.x + bar_length, self.y), 
                             (self.x + bar_length, self.y + self.height), (self.x, self.y + self.height)], 
                            2, "Black", bar_color)

        #If health is 0, overlay a full red bar
        if self.health == 0:
            canvas.draw_polygon([(self.x, self.y), (self.x + self.width, self.y), 
                                 (self.x + self.width, self.y + self.height), (self.x, self.y + self.height)], 
                                2, "Black", "Red")

        #Display health percentage
        canvas.draw_text(f"{self.health}%", (self.x + 130, self.y + 20), 18, "White")

#Initialize health bar
player_health_bar = HealthBar(MAX_HEALTH, BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT)

def take_damage():
    player_health_bar.take_damage(20)

def draw(canvas):
    player_health_bar.draw(canvas)

frame = simplegui.create_frame("Health Bar", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
#Add button to take damage -- needs to be editted so when player is damaged then health decreases 
frame.add_button("Take Damage", take_damage, 100)
frame.start()
