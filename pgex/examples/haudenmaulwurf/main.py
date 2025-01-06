import pygame
import random
import time
import asyncio

# Screen dimensions
# TODO do not make global
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Colors / Fonts
# TODO move to classes
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
MOLE_COLORS = [(139, 69, 19), (160, 82, 45), (205, 133, 63)]

def fade_to_color(screen: pygame.Surface, color: pygame.typing.ColorLike):
    fade_surface = pygame.Surface(screen.get_rect().size)
    fade_surface.fill(color)
    for alpha in range(0, 256, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)

class Hammer:
    img: pygame.Surface

    def __init__(self):
        img_unscaled = pygame.image.load('pgex/examples/haudenmaulwurf/hammer.png')
        self.img = pygame.transform.scale(img_unscaled, (50, 50))

    def draw(self, screen):
        rect = self.img.get_rect()
        rect.center = pygame.mouse.get_pos()
        screen.blit(self.img, rect.topleft)

class Mole:
    def __init__(self, pos, level):
        self.pos = pos
        self.color = random.choice(MOLE_COLORS)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 3000 // level

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, 30)

    def is_hit(self, pos):
        return pygame.Rect(self.pos[0] - 30, self.pos[1] - 30, 60, 60).collidepoint(pos)


class Game():
    clock = pygame.time.Clock()
    holes = [(x, y) for x in range(100, 701, 150) for y in range(100, 501, 150)]
    moles = []
    score = 0
    lives = 3
    level = 1
    mole_timer = 1000
    level_timer = 30000
    last_mole_time = pygame.time.get_ticks()
    last_level_time = pygame.time.get_ticks()
    font: pygame.Font
    hammer: Hammer = Hammer()
    screen: pygame.Surface
    running: bool

    def __init__(self, screen):
        self.font = pygame.font.Font(None, 36)
        self.screen = screen

    def draw_score(self, screen, score):
        score_text = self.font.render(f"Score: {score}", True, BLUE)
        screen.blit(score_text, (SCREEN_WIDTH - 150, 10))

    def draw_lives(self, screen, lives):
        lives_text = self.font.render(f"Lives: {lives}", True, RED)
        screen.blit(lives_text, (10, 10))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for mole in self.moles[:]:
                    if mole.is_hit(event.pos):
                        self.score += self.level
                        self.moles.remove(mole)

    def game_over_animation(self, screen: pygame.Surface):
        fade_to_color(screen, BLACK)

        font_large = pygame.font.Font(None, 72)
        game_over_text = font_large.render("Du bist tot", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        # Draw gravestone
        pygame.draw.rect(screen, (169, 169, 169), (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, 100, 150))
        pygame.draw.rect(screen, (105, 105, 105), (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 + 10, 80, 130))
        pygame.draw.rect(screen, (169, 169, 169), (SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2 + 20, 60, 110))
        pygame.draw.rect(screen, (105, 105, 105), (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 + 30, 40, 90))

        pygame.display.flip()
        time.sleep(5)

        fade_to_color(screen, BLUE)


    def run(self):
        """_summary_ main game loop
        """
        self.running = True
        while self.running:
            self.screen.fill(WHITE)
            current_time = pygame.time.get_ticks()

            # Check for level up
            if current_time - self.last_level_time > self.level_timer:
                self.level += 1
                self.lives += 1
                self.mole_timer = max(100, self.mole_timer - 100)
                self.last_level_time = current_time

            # Spawn new mole
            if current_time - self.last_mole_time > self.mole_timer:
                if len(self.moles) < 16:
                    new_mole = Mole(random.choice(self.holes), self.level)
                    self.moles.append(new_mole)
                self.last_mole_time = current_time

            # Draw moles and check for expired moles
            for mole in self.moles[:]:
                if current_time - mole.spawn_time > mole.lifetime:
                    self.moles.remove(mole)
                    self.lives -= 1
                else:
                    mole.draw(self.screen)

            self.draw_score(self.screen, self.score)
            self.draw_lives(self.screen, self.lives)
            self.hammer.draw(self.screen)

            self.handle_events()

            pygame.display.flip()
            self.clock.tick(60)

            # Game over check
            if self.lives <= 0:
                self.game_over_animation(self.screen)
                self.running = False


class StartMenu():
    font : pygame.Font
    screen: pygame.Surface

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)

    def run(self):
        menu_running = True
        while menu_running:
            self.screen.fill(BLUE)
            font_large = pygame.font.Font(None, 72)
            title_text = font_large.render("Whack-a-Mole", True, WHITE)
            new_game_text = self.font.render("Neues Spiel", True, WHITE)
            quit_text = self.font.render("Beenden", True, WHITE)
            
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 150))
            self.screen.blit(new_game_text, (SCREEN_WIDTH // 2 - new_game_text.get_width() // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if new_game_text.get_rect(topleft=(SCREEN_WIDTH // 2 - new_game_text.get_width() // 2, SCREEN_HEIGHT // 2)).collidepoint(mouse_pos):
                        fade_to_color(self.screen, WHITE)
                        Game(self.screen).run()
                    elif quit_text.get_rect(topleft=(SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50)).collidepoint(mouse_pos):
                        menu_running = False


async def main() -> None:
    pygame.init()
    pygame.display.set_caption("Whack-a-Mole")
    screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(screen_size)
    StartMenu(screen).run()
    pygame.quit()
    exit()             
    
def run():
    asyncio.run(main())

if __name__ == "__main__":
     run()
