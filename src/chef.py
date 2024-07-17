import pygame
from src.utils import pathfind

class Chef:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.position = (0, 0)
        self.target = None
        self.image = pygame.image.load('assets/Chef.png')
        self.path = []
        self.state = 'idle'  # states: idle, getting_ingredients, cooking, plating

    def update(self):
        if self.state == 'idle':
            pass
        elif self.state == 'getting_ingredients':
            pass  # Implement ingredient gathering behavior
        elif self.state == 'cooking':
            pass  # Implement cooking behavior
        elif self.state == 'plating':
            pass  # Implement plating behavior

    def draw(self, screen, assets):
        screen.blit(assets['chef'], (self.position[0], self.position[1] - (self.image.get_height() - self.grid_size) // 2))
