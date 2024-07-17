import pygame
import json

class MapManager:
    def __init__(self, grid_size, max_grid_x, max_grid_y):
        self.grid_size = grid_size
        self.max_grid_x = max_grid_x
        self.max_grid_y = max_grid_y
        self.game_map = [[None for _ in range(max_grid_x)] for _ in range(max_grid_y)]
        self.chairs = {}
        self.tables = {}
        self.load_map()

    def load_map(self, filename='data/map.json'):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.game_map = data['game_map']
                self.chairs = {tuple(map(int, key.split(','))): value for key, value in data['chairs'].items()}
                self.tables = {tuple(map(int, key.split(','))): value for key, value in data['tables'].items()}
                
                # Reset taken attribute for all tables and chairs
                for key in self.chairs:
                    self.chairs[key]['taken'] = False
                for key in self.tables:
                    self.tables[key]['taken'] = False
        except FileNotFoundError:
            pass

    def save_map(self, filename='data/map.json'):
        data = {
            'game_map': self.game_map,
            'chairs': {f"{key[0]},{key[1]}": value for key, value in self.chairs.items()},
            'tables': {f"{key[0]},{key[1]}": value for key, value in self.tables.items()}
        }
        with open(filename, 'w') as f:
            json.dump(data, f)

    def draw_floor(self, screen, assets):
        for x in range(0, self.max_grid_x * self.grid_size, self.grid_size):
            for y in range(0, self.max_grid_y * self.grid_size, self.grid_size):
                if self.is_border(x // self.grid_size, y // self.grid_size):
                    screen.blit(assets['wall'], (x, y))
                else:
                    screen.blit(assets['floor'], (x, y))

    def is_border(self, grid_x, grid_y):
        return grid_x == 0 or grid_y == 0 or grid_x == self.max_grid_x - 1 or grid_y == self.max_grid_y - 1

    def draw_chairs(self, screen, assets):
        for (x, y), chair in self.chairs.items():
            if chair['type']:
                screen.blit(assets[chair['type']], (x * self.grid_size, y * self.grid_size))

    def draw_tables(self, screen, assets):
        for (x, y), table in self.tables.items():
            if table['type']:
                screen.blit(assets[table['type']], (x * self.grid_size, y * self.grid_size))

    def place_item(self, item, mouse_x, mouse_y):
        grid_x = int(mouse_x) // self.grid_size
        grid_y = int(mouse_y) // self.grid_size

        # Check if the grid coordinates are within the valid range
        if 0 <= grid_x < self.max_grid_x and 0 <= grid_y < self.max_grid_y:
            if item == 'chair':
                if self.game_map[grid_y][grid_x] is None and (grid_x, grid_y) not in self.tables:
                    self.chairs[(grid_x, grid_y)] = {'type': 'chair', 'taken': False}
                    self.game_map[grid_y][grid_x] = item
                    print(f"Placed chair at ({grid_x}, {grid_y})")
                else:
                    print("Obstructed location: cannot place chair here")
            elif item == 'table':
                if self.game_map[grid_y][grid_x] is None and (grid_x, grid_y) not in self.chairs:
                    self.tables[(grid_x, grid_y)] = {'type': 'table', 'taken': False}
                    self.game_map[grid_y][grid_x] = item
                    print(f"Placed table at ({grid_x}, {grid_y})")
                else:
                    print("Obstructed location: cannot place table here")
        else:
            print("Invalid location: outside map boundaries")

    def delete_item(self, mouse_x, mouse_y):
        grid_x = int(mouse_x) // self.grid_size
        grid_y = int(mouse_y) // self.grid_size
        if 0 <= grid_x < self.max_grid_x and 0 <= grid_y < self.max_grid_y:
            if (grid_x, grid_y) in self.chairs:
                del self.chairs[(grid_x, grid_y)]
                print(f"Deleted chair at ({grid_x, grid_y})")
            elif (grid_x, grid_y) in self.tables:
                del self.tables[(grid_x, grid_y)]
                print(f"Deleted table at ({grid_x, grid_y})")
            self.game_map[grid_y][grid_x] = None
        else:
            print("Invalid location: outside map boundaries")

    def find_available_tables(self, customers):
        available_tables = []
        for (x, y), table in self.tables.items():
            if not table['taken']:
                seats = []
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) in self.chairs and not self.chairs[(nx, ny)]['taken']:
                        seats.append((nx, ny))
                if seats:
                    available_tables.append(((x, y), seats))
        print(f"Available tables: {available_tables}")
        return available_tables

    def mark_table_taken(self, table, seats):
        x, y = table
        self.tables[(x, y)]['taken'] = True
        for seat in seats:
            self.chairs[seat]['taken'] = True
        print(f"Marked table at ({x, y}) and seats {seats} as taken")

    def get_obstacles(self):
        obstacles = set()
        for (x, y) in self.tables.keys():
            obstacles.add((x, y))
        for (x, y) in self.chairs.keys():
            obstacles.add((x, y))
        print(f"Obstacles: {obstacles}")
        return obstacles
