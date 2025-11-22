import pygame
from random import choice, randrange

# Constants
RES = WIDTH, HEIGHT = 600, 600
TILE = 20
cols, rows = WIDTH // TILE, HEIGHT // TILE
FPS = 50

# Pygame setup
pygame.init()
sc = pygame.display.set_mode(RES)
pygame.display.set_caption("Hunt and Kill Maze Generator")
clock = pygame.time.Clock()

# Cell class
class cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color("#f70067"), (x + 2, y + 2, TILE - 2, TILE - 2), border_radius=5)

    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, pygame.Color("#1e1e1e"), (x, y, TILE, TILE))
        if self.walls['top']:
            pygame.draw.line(sc, (0,255,0), (x,y), (x + TILE, y), 3)
        if self.walls['right']:
            pygame.draw.line(sc, (0,255,0), (x + TILE, y), (x + TILE, y + TILE), 3)
        if self.walls['bottom']:
            pygame.draw.line(sc, (0,255,0), (x + TILE, y + TILE), (x, y + TILE), 3)
        if self.walls['left']:
            pygame.draw.line(sc, (0,255,0), (x, y + TILE), (x, y), 2)

    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x >= cols or y < 0 or y >= rows:
            return None
        return grid_cells[find_index(x, y)]

    def unvisited_neighbors(self):
        neighbors = []
        for dx, dy in [(0,-1), (1,0), (0,1), (-1,0)]:
            neighbor = self.check_cell(self.x + dx, self.y + dy)
            if neighbor and not neighbor.visited:
                neighbors.append(neighbor)
        return neighbors

def remove_walls(a, b):
    dx = a.x - b.x
    dy = a.y - b.y
    if dx == 1:
        a.walls['left'] = False
        b.walls['right'] = False
    elif dx == -1:
        a.walls['right'] = False
        b.walls['left'] = False
    if dy == 1:
        a.walls['top'] = False
        b.walls['bottom'] = False
    elif dy == -1:
        a.walls['bottom'] = False
        b.walls['top'] = False

# Grid setup
grid_cells = [cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[randrange(len(grid_cells))]
current_cell.visited = True
mode = 'kill'

# Main loop
while True:
    sc.fill(pygame.Color('#a6d5e2'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    [c.draw() for c in grid_cells]
    current_cell.draw_current_cell()

    if mode == 'kill':
        neighbors = current_cell.unvisited_neighbors()
        if neighbors:
            next_cell = choice(neighbors)
            remove_walls(current_cell, next_cell)
            next_cell.visited = True
            current_cell = next_cell
        else:
            mode = 'hunt'

    elif mode == 'hunt':
        found = False
        for y in range(rows):
            for x in range(cols):
                cell_ = grid_cells[x + y * cols]
                if not cell_.visited:
                    visited_neighbors = [n for n in [
                        cell_.check_cell(cell_.x, cell_.y - 1),
                        cell_.check_cell(cell_.x + 1, cell_.y),
                        cell_.check_cell(cell_.x, cell_.y + 1),
                        cell_.check_cell(cell_.x - 1, cell_.y)
                    ] if n and n.visited]
                    if visited_neighbors:
                        neighbor = choice(visited_neighbors)
                        remove_walls(cell_, neighbor)
                        cell_.visited = True
                        current_cell = cell_
                        mode = 'kill'
                        found = True
                        break
            if found:
                break
        if not found:
            mode = 'done'

    pygame.display.flip()
    clock.tick(FPS)