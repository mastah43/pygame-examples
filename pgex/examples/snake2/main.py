import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont(None, 36)

# Snake class
class Snake:
    def __init__(self):
        self.positions = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.grow = False

    def move(self):
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x * CELL_SIZE, head_y + dir_y * CELL_SIZE)
        
        # Check if the snake hits the wall
        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in self.positions):
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if not self.grow:
                self.positions.pop()
            self.grow = False

    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction
            global score
            score += 5

    def reset(self):
        global death_count, score
        death_count += 1
        score = 0
        self.__init__()

    def draw(self, surface):
        for pos in self.positions:
            pygame.draw.rect(surface, GREEN, (*pos, CELL_SIZE, CELL_SIZE))

    def grow_snake(self):
        self.grow = True
        global score
        score += 50

# Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                         random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (*self.position, CELL_SIZE, CELL_SIZE))

# Main game loop
def main():
    global death_count, score
    death_count = 0
    score = 0
    snake = Snake()
    food = Food()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    snake.change_direction(UP)
                elif event.key == pygame.K_s:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_a:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_d:
                    snake.change_direction(RIGHT)

        snake.move()
        if snake.positions[0] == food.position:
            snake.grow_snake()
            food.randomize_position()

        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)

        # Draw death count
        death_text = font.render(f"Tode: {death_count}", True, WHITE)
        screen.blit(death_text, (10, 10))

        # Draw score
        score_text = font.render(f"Punkte: {score}", True, BLUE)
        screen.blit(score_text, (WIDTH - 150, 10))

        pygame.display.flip()
        clock.tick(10)
        score += 1  # Increment score for each second survived

    pygame.quit()

if __name__ == "__main__":
    main()
    def draw_star(surface, position, color, size):
        points = [
            (position[0], position[1] - size),
            (position[0] + size * 0.5, position[1] - size * 0.5),
            (position[0] + size, position[1]),
            (position[0] + size * 0.5, position[1] + size * 0.5),
            (position[0], position[1] + size),
            (position[0] - size * 0.5, position[1] + size * 0.5),
            (position[0] - size, position[1]),
            (position[0] - size * 0.5, position[1] - size * 0.5),
        ]
        pygame.draw.polygon(surface, color, points)

    def main():
        global death_count, score
        death_count = 0
        score = 0
        snake = Snake()
        food = Food()
        running = True
        show_star = False
        star_timer = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        snake.change_direction(UP)
                    elif event.key == pygame.K_s:
                        snake.change_direction(DOWN)
                    elif event.key == pygame.K_a:
                        snake.change_direction(LEFT)
                    elif event.key == pygame.K_d:
                        snake.change_direction(RIGHT)

            snake.move()
            if snake.positions[0] == food.position:
                snake.grow_snake()
                food.randomize_position()

            screen.fill(BLACK)
            snake.draw(screen)
            food.draw(screen)

            # Draw death count
            death_text = font.render(f"Tode: {death_count}", True, WHITE)
            screen.blit(death_text, (10, 10))

            # Draw score
            score_text = font.render(f"Punkte: {score}", True, BLUE)
            screen.blit(score_text, (WIDTH - 150, 10))

            # Show star animation every 500 points
            if score % 500 == 0 and score != 0:
                show_star = True
                star_timer = pygame.time.get_ticks()

            if show_star:
                draw_star(screen, (WIDTH // 2, HEIGHT // 2), WHITE, 30)
                if pygame.time.get_ticks() - star_timer > 1000:  # Show star for 1 second
                    show_star = False

            pygame.display.flip()
            clock.tick(10)
            score += 1  # Increment score for each second survived

        pygame.quit()

    if __name__ == "__main__":
        main()