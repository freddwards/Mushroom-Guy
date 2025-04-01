from PIL.TiffImagePlugin import ROWSPERSTRIP

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.5
JUMP_POWER = -10
TERMINAL_VELOCITY = 10
PLAYER_SPEED = 5
DEFAULT_PLAYER_SPEED = 5
SLOW_FACTOR = 0.3
LIVES = 3
HEART_IMAGE_URL = "https://i.ibb.co/rG6G79Hj/Untitled.jpg"
HEART_IMAGE_SIZE = (25, 25)
HEART_IMAGE_SPACING = 7
TILE_SIZE = 24
TILE_TYPES = 23
POWERUP_SIZE = 24
POWERUP_TYPES = 3
SCROLL_THRESH_X = 300
SCROLL_THRESH_Y = 250

ROWS = 5
COLS = 6

PLAYER = {
    "x": SCREEN_WIDTH // 2,
    "y": SCREEN_HEIGHT - 40,
    "vx": 0,
    "vy": 0,
    "size": 20,
    "direction": "left",
}
