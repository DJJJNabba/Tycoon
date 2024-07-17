import pygame
import random

class Customer:
    def __init__(self, grid_size, start_pos, end_pos, screen_width, screen_height):
        self.grid_size = grid_size
        self.position = start_pos
        self.end_pos = end_pos
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load('assets/Customer.png')
        self.speed = 1.2  # Speed of the customer
        self.state = 'seating'
        self.spawn_x = (self.screen_width // 2 // self.grid_size) * self.grid_size
        self.spawn_y = self.screen_height - self.grid_size
        self.wait_time = 0

        # Calculate the direction to move towards the end position
        self.direction = (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
        distance = (self.direction[0]**2 + self.direction[1]**2) ** 0.5
        self.direction = (self.direction[0] / distance, self.direction[1] / distance)

    def update(self):
        if self.state == 'seating':
            print("seating")
            # Move the customer towards the end position
            self.position = (
                self.position[0] + self.direction[0] * self.speed,
                self.position[1] + self.direction[1] * self.speed,
            )
            # Check if the customer has reached the destination
            if ((self.position[0] - self.end_pos[0])**2 + (self.position[1] - self.end_pos[1])**2) ** 0.5 < self.speed:
                self.position = self.end_pos
                self.state = 'seated'

        elif self.state == 'seated':
            print("seated")
            self.wait_time += 1
            if self.wait_time > 300:  # 5 seconds
                self.state = 'ordering'

        elif self.state == 'ordering':
            print("ordering")
            self.order = (random.choice(['water', 'coke']), random.choice(['hotdog', 'pizza']))
            print(self.order)
            self.state = 'waiting'

        elif self.state == 'waiting':
            print("waiting")
            pass  # Wait for food to be served

        elif self.state == 'eating':
            print("eating")
            self.wait_time += 1
            if self.wait_time > 480:  # 8 seconds
                self.state = 'leaving'
                self.wait_time = 0

        elif self.state == 'leaving':
            self.end_pos = (self.spawn_x, self.spawn_y)
            self.direction = (self.end_pos[0] - self.position[0], self.end_pos[1] - self.position[1])
            distance = (self.direction[0]**2 + self.direction[1]**2) ** 0.5
            self.direction = (self.direction[0] / distance, self.direction[1] / distance)

            self.position = (
                self.position[0] + self.direction[0] * self.speed,
                self.position[1] + self.direction[1] * self.speed,
            )
            # Check if the customer has reached the destination
            if ((self.position[0] - self.end_pos[0])**2 + (self.position[1] - self.end_pos[1])**2) ** 0.5 < self.speed:
                self.position = self.end_pos
                self.state = 'done'

    def draw(self, screen):
        screen.blit(self.image, (self.position[0], self.position[1] - (self.image.get_height() - self.grid_size) // 2))

    def is_done(self):
        return self.state == 'done'
