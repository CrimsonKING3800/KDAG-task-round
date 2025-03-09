import pygame
import random

class Config:
    WIDTH = 800
    HEIGHT = 800
    GRID_SIZE = 10
    ROWS = WIDTH // GRID_SIZE
    COLS = HEIGHT // GRID_SIZE
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    FPS = 30
    SELF_PHEROMONE_PROB = 0.8
    CROSS_PHEROMONE_PROB = 0.2
    DECAY_PROB = 0.2

class Ant:
    def __init__(self, x=None, y=None, direction=None, pheromone_type='A'):
        self.x = x if x is not None else random.randint(0, Config.ROWS - 1)
        self.y = y if y is not None else random.randint(0, Config.COLS - 1)
        self.direction = direction if direction is not None else random.randint(0, 3)
        self.pheromone_type = pheromone_type

    def move(self, grid, pheromones):
        current_color = grid.get_color(self.x, self.y)
        phero_here = pheromones.get_pheromone(self.x, self.y)

        # Determine direction based on pheromone influence
        if phero_here == self.pheromone_type:  # Self pheromone
            if random.random() < Config.SELF_PHEROMONE_PROB:
                pass  # Keep same direction
            else:
                self.turn(current_color)
        elif phero_here:  # Cross pheromone
            if random.random() < Config.CROSS_PHEROMONE_PROB:
                pass  # Keep same direction
            else:
                self.turn(current_color)
        else:  # Normal behavior
            self.turn(current_color)

        # Flip color and set pheromone
        grid.flip_color(self.x, self.y)
        pheromones.set_pheromone(self.x, self.y, self.pheromone_type)

        # Move forward
        self.move_forward()

    def turn(self, current_color):
        if current_color == Config.WHITE:
            self.direction = (self.direction + 1) % 4
        else:
            self.direction = (self.direction - 1) % 4

    def move_forward(self):
        if self.direction == 0: self.y -= 1
        elif self.direction == 1: self.x += 1
        elif self.direction == 2: self.y += 1
        elif self.direction == 3: self.x -= 1
        
        self.x %= Config.ROWS
        self.y %= Config.COLS

class Grid:
    def __init__(self):
        self.cells = {}

    def get_color(self, x, y):
        return self.cells.get((x, y), Config.WHITE)

    def flip_color(self, x, y):
        self.cells[(x, y)] = Config.BLACK if self.get_color(x, y) == Config.WHITE else Config.WHITE

    def draw(self, screen):
        for (x, y), color in self.cells.items():
            pygame.draw.rect(screen, color, 
                           (x * Config.GRID_SIZE, y * Config.GRID_SIZE, 
                            Config.GRID_SIZE, Config.GRID_SIZE))

class PheromoneSystem:
    def __init__(self):
        self.pheromones = {}

    def get_pheromone(self, x, y):
        return self.pheromones.get((x, y))

    def set_pheromone(self, x, y, pheromone):
        self.pheromones[(x, y)] = pheromone

    def decay(self):
        to_remove = [pos for pos in self.pheromones if random.random() < Config.DECAY_PROB]
        for pos in to_remove:
            del self.pheromones[pos]

    def draw(self, screen):
        for (x, y), phero in self.pheromones.items():
            color = Config.RED if phero == 'A' else Config.BLUE
            pygame.draw.rect(screen, color, 
                           (x * Config.GRID_SIZE, y * Config.GRID_SIZE, 
                            Config.GRID_SIZE, Config.GRID_SIZE), 1)

class Simulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        pygame.display.set_caption("Langton's Ant Problem")
        self.clock = pygame.time.Clock()
        
        self.grid = Grid()
        self.pheromones = PheromoneSystem()
        self.ants = [Ant(pheromone_type='A'), Ant(pheromone_type='B')]

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(Config.WHITE)
            
            # Update
            for ant in self.ants:
                ant.move(self.grid, self.pheromones)
            self.pheromones.decay()
            
            # Draw
            self.grid.draw(self.screen)
            self.pheromones.draw(self.screen)
            
            # Draw ants
            for ant in self.ants:
                pygame.draw.rect(self.screen, Config.GREEN, 
                               (ant.x * Config.GRID_SIZE, ant.y * Config.GRID_SIZE, 
                                Config.GRID_SIZE, Config.GRID_SIZE))
            
            pygame.display.flip()
            self.clock.tick(Config.FPS)

        pygame.quit()

if __name__ == "__main__":
    simulation = Simulation()
    simulation.run()
