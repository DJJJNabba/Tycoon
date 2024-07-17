import pygame
from src.utils import pathfind

class Waiter:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.position = (0, 0)
        self.target = None
        self.image = pygame.image.load('assets/Waiter.png')
        self.path = []
        self.state = 'idle'  # states: idle, taking_order, delivering_order, clearing_table

    def update(self):
        if self.state == 'idle':
            pass
        elif self.state == 'taking_order':
            pass  # Implement order taking behavior
        elif self.state == 'delivering_order':
            pass  # Implement order delivering behavior
        elif self.state == 'clearing_table':
            pass  # Implement table clearing behavior

    def draw(self, screen, assets):
        screen.blit(assets['waiter'], (self.position[0], self.position[1] - (self.image.get_height() - self.grid_size) // 2))
