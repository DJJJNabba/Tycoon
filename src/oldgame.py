import pygame
import sys
import json

# Initialize Pygame
pygame.init()

# Screen dimensions and grid size
screen_width = 640
screen_height = 480
grid_size = 32
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Restaurant Tycoon')

# Load images
assets = {
    'chair': pygame.image.load('img/assets/Chair.png'),
    'table': pygame.image.load('img/assets/Table.png'),
    'counter': pygame.image.load('img/assets/Counter.png'),
    'floor': pygame.image.load('img/assets/Floor.png')
}

# Create a map to store placed items
game_map = [[None for _ in range(screen_width // grid_size)] for _ in range(screen_height // grid_size)]

# Save and load functions
def save_map(filename='map.json'):
    with open(filename, 'w') as f:
        json.dump(game_map, f)

def load_map(filename='map.json'):
    global game_map
    try:
        with open(filename, 'r') as f:
            game_map = json.load(f)
    except FileNotFoundError:
        pass

# Load the map if it exists
load_map()

# Function to draw the floor
def draw_floor():
    for x in range(0, screen_width, grid_size):
        for y in range(0, screen_height, grid_size):
            screen.blit(assets['floor'], (x, y))

# Function to draw the map items
def draw_map():
    for y, row in enumerate(game_map):
        for x, item in enumerate(row):
            if item:
                screen.blit(assets[item], (x * grid_size, y * grid_size))

# Function to place an item at the mouse position
def place_item(item):
    x, y = pygame.mouse.get_pos()
    grid_x = x // grid_size
    grid_y = y // grid_size
    if game_map[grid_y][grid_x] is None:
        game_map[grid_y][grid_x] = item

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                place_item('table')
            elif event.button == 3:  # Right click
                place_item('chair')
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:  # Press 'C'
                place_item('counter')

    # Draw everything
    draw_floor()
    draw_map()
    pygame.display.flip()

# Save the map when the game exits
save_map()

pygame.quit()
sys.exit()
