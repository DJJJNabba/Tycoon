import pygame
import random
from src.map_manager import MapManager
from src.customer import Customer
from src.waiter import Waiter
from src.chef import Chef

class Game:
    def __init__(self):
        self.screen_width = 640
        self.screen_height = 480
        self.grid_size = 32
        self.SCALE_FACTOR = 1  # Initial scaling factor (no scaling at start)
        self.max_scale = 2  # Maximum zoom in
        self.min_scale = 0.5  # Maximum zoom out
        self.pan_offset = [0, 0]  # Initial pan offset
        self.pan_active = False
        self.pan_start = [0, 0]

        self.max_grid_x = 30
        self.max_grid_y = 45

        self.scaled_width = int(self.screen_width * self.SCALE_FACTOR)
        self.scaled_height = int(self.screen_height * self.SCALE_FACTOR)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.scaled_surface = pygame.Surface((self.scaled_width, self.scaled_height))

        pygame.display.set_caption('Restaurant Tycoon')
        self.clock = pygame.time.Clock()
        self.running = True
        self.map_manager = MapManager(self.grid_size, self.max_grid_x, self.max_grid_y)
        self.customers = []
        self.waiter = Waiter(self.grid_size)
        self.chef = Chef(self.grid_size)
        self.publicity = 1  # Initialize publicity variable
        self.spawn_timer = 0
        self.load_assets()

    def load_assets(self):
        self.assets = {
            'chair': pygame.image.load('assets/Chair.png'),
            'table': pygame.image.load('assets/Table.png'),
            'counter': pygame.image.load('assets/Counter.png'),
            'floor': pygame.image.load('assets/Floor.png'),
            'wall': pygame.image.load('assets/Wall.png'),  # Wall texture
            'customer': pygame.image.load('assets/Customer.png'),
            'waiter': pygame.image.load('assets/Waiter.png'),
            'chef': pygame.image.load('assets/Chef.png'),
        }

    def run(self):
        try:
            while self.running:
                self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(60)
        finally:
            self.map_manager.save_map()  # Ensure map is saved when the game exits

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.pan_active = True
                    print("panning with mouse down")
                    self.pan_start = list(event.pos)
                elif event.button == 4:  # Scroll up
                    self.zoom_in(event.pos)
                elif event.button == 5:  # Scroll down
                    self.zoom_out(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left click
                    print("stopped panning")
                    self.pan_active = False
                    mouse_x, mouse_y = self.convert_mouse_position(event.pos)
                    if self.within_bounds(mouse_x, mouse_y):
                        self.map_manager.place_item('table', mouse_x, mouse_y)
            elif event.type == pygame.MOUSEMOTION:
                if self.pan_active:
                    print("moving with pan")
                    dx, dy = event.pos[0] - self.pan_start[0], event.pos[1] - self.pan_start[1]
                    self.pan_offset[0] += dx
                    self.pan_offset[1] += dy
                    self.pan_start = list(event.pos)
                    self.clamp_pan()
            elif event.type == pygame.KEYDOWN:
                mouse_x, mouse_y = self.convert_mouse_position(pygame.mouse.get_pos())
                if event.key == pygame.K_c:  # Press 'C'
                    if self.within_bounds(mouse_x, mouse_y):
                        self.map_manager.place_item('counter', mouse_x, mouse_y)
                elif event.key == pygame.K_BACKSPACE:  # Press 'Backspace'
                    if self.within_bounds(mouse_x, mouse_y):
                        self.map_manager.delete_item(mouse_x, mouse_y)
                elif event.key == pygame.K_t:
                    if self.within_bounds(mouse_x, mouse_y):
                        self.map_manager.place_item('table', mouse_x, mouse_y)
                elif event.key == pygame.K_s:
                    if self.within_bounds(mouse_x, mouse_y):
                        self.map_manager.place_item('chair', mouse_x, mouse_y)

    def convert_mouse_position(self, pos):
        # Convert mouse position from scaled surface to original surface
        x = (pos[0] - self.pan_offset[0]) / self.SCALE_FACTOR
        y = (pos[1] - self.pan_offset[1]) / self.SCALE_FACTOR
        return int(x), int(y)

    def within_bounds(self, x, y):
        return 0 <= x < self.max_grid_x * self.grid_size and 0 <= y < self.max_grid_y * self.grid_size

    def clamp_pan(self):
        # Prevent panning outside the borders
        max_x = self.max_grid_x * self.grid_size * self.SCALE_FACTOR - self.screen_width
        max_y = self.max_grid_y * self.grid_size * self.SCALE_FACTOR - self.screen_height
        self.pan_offset[0] = max(min(self.pan_offset[0], 0), -max_x)
        self.pan_offset[1] = max(min(self.pan_offset[1], 0), -max_y)

    def zoom_in(self, mouse_pos):
        if self.SCALE_FACTOR < self.max_scale:
            old_scale = self.SCALE_FACTOR
            self.SCALE_FACTOR += 0.1
            self.zoom(mouse_pos, old_scale)

    def zoom_out(self, mouse_pos):
        if self.SCALE_FACTOR > self.min_scale:
            old_scale = self.SCALE_FACTOR
            self.SCALE_FACTOR -= 0.1
            self.zoom(mouse_pos, old_scale)

    def zoom(self, mouse_pos, old_scale):
        # Get mouse position on the scaled surface
        mx, my = mouse_pos
        mx = (mx - self.pan_offset[0]) / old_scale
        my = (my - self.pan_offset[1]) / old_scale

        # Update the scaling
        self.update_scaled_surface()

        # Adjust pan offset to zoom relative to the mouse cursor
        self.pan_offset[0] = mx * self.SCALE_FACTOR - mouse_pos[0]
        self.pan_offset[1] = my * self.SCALE_FACTOR - mouse_pos[1]
        self.clamp_pan()

    def update_scaled_surface(self):
        self.scaled_width = int(self.screen_width * self.SCALE_FACTOR)
        self.scaled_height = int(self.screen_height * self.SCALE_FACTOR)
        self.scaled_surface = pygame.Surface((self.scaled_width, self.scaled_height))
        self.clamp_pan()

    def update(self):
        self.spawn_timer += 1
        if self.spawn_timer >= 480:  # Every 8 seconds
            self.spawn_timer = 0
            self.spawn_group()
        self.waiter.update()
        self.chef.update()
        for customer in self.customers:
            customer.update()

        # Remove customers that are done
        self.customers = [customer for customer in self.customers if not customer.is_done()]

    def draw(self):
        self.scaled_surface.fill((0, 0, 0))  # Clear the scaled surface
        self.map_manager.draw_floor(self.scaled_surface, self.assets)
        self.map_manager.draw_chairs(self.scaled_surface, self.assets)
        for customer in self.customers:
            customer.draw(self.scaled_surface)
        self.map_manager.draw_tables(self.scaled_surface, self.assets)
        self.waiter.draw(self.scaled_surface, self.assets)
        self.chef.draw(self.scaled_surface, self.assets)

        # Scale the surface to fit the window
        scaled_surface = pygame.transform.scale(self.scaled_surface, (self.screen_width, self.screen_height))
        self.screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()

    def spawn_group(self):
        available_tables = self.map_manager.find_available_tables(self.customers)
        if available_tables:
            table, seats = random.choice(available_tables)
            spawn_x = (self.screen_width // 2 // self.grid_size) * self.grid_size
            spawn_y = self.screen_height - self.grid_size
            for seat in seats:
                self.customers.append(Customer(self.grid_size, (spawn_x, spawn_y), (seat[0] * self.grid_size, seat[1] * self.grid_size), self.screen_width, self.screen_height))
                print(f"Spawning customer at seat {seat}")
            self.map_manager.mark_table_taken(table, seats)
