import pygame

# Window settings
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 360

# Global settings
GAME_NAME = 'Snake'
GLOBAL_FPS = 60
GRID_SIZE = 10

# Gameplay settings
SNAKE_SPEED = 20
SNAKE_INIT_LENGTH = 0
SNAKE_INIT_X = WINDOW_WIDTH // 5 // GRID_SIZE * GRID_SIZE
SNAKE_INIT_Y = WINDOW_HEIGHT // 2 // GRID_SIZE * GRID_SIZE

# Colors (R, G, B)
RGB = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'SNAKE': (0, 165, 80),
    'BLOOD': (152, 0, 2),
    'APPLE': (110, 203, 60),
}

# Key assignment
KEYS = {
    'LEFT': pygame.K_LEFT,
    'RIGHT': pygame.K_RIGHT,
    'UP': pygame.K_UP,
    'DOWN': pygame.K_DOWN,
}
