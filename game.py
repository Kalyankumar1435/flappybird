import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird (Python)")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.Font("freesansbold.ttf", 32)
big_font = pygame.font.Font("freesansbold.ttf", 48)

# Game variables
gravity = 0.5
bird_movement = 0
pipe_width = 60
pipe_gap = 150
pipe_speed = 4


def create_pipe():
    y_pos = random.randint(100, 400)
    top_pipe = pygame.Rect(WIDTH, y_pos - pipe_gap // 2 - HEIGHT, pipe_width, HEIGHT)
    bottom_pipe = pygame.Rect(WIDTH, y_pos + pipe_gap // 2, pipe_width, HEIGHT)
    return top_pipe, bottom_pipe

def draw_text(text, font, color, x, y, center=True):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(img, rect)

def game_loop():
    global bird_movement

    bird = pygame.Rect(50, HEIGHT // 2, 40, 40)
    bird_movement = 0
    score = 0
    pipes = []
    pipes.extend(create_pipe())

    while True:
        clock.tick(FPS)
        screen.fill(BLUE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_movement = -10

        # Bird movement
        bird_movement += gravity
        bird.y += bird_movement

        # Draw bird (as a ball)
        pygame.draw.circle(screen, WHITE, bird.center, 20)

        # Move and draw pipes
        for pipe in pipes:
            pipe.x -= pipe_speed
            pygame.draw.rect(screen, GREEN, pipe)

        # Remove off-screen pipes and add new ones
        if pipes[0].x < -pipe_width:
            pipes.pop(0)
            pipes.pop(0)
            pipes.extend(create_pipe())
            score += 1

        # Collision detection
        for pipe in pipes:
            if bird.colliderect(pipe):
                return score

        if bird.top <= 0 or bird.bottom >= HEIGHT:
            return score

        # Draw score
        draw_text(f"Score: {score}", font, WHITE, 10, 10, center=False)

        pygame.display.update()

def start_screen():
    while True:
        screen.fill(BLUE)
        draw_text("Flappy Bird", big_font, WHITE, WIDTH // 2, HEIGHT // 3)
        draw_text("Press SPACE to Start", font, WHITE, WIDTH // 2, HEIGHT // 2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def game_over_screen(score):
    while True:
        screen.fill(BLUE)
        draw_text("Game Over", big_font, RED, WIDTH // 2, HEIGHT // 3)
        draw_text(f"Score: {score}", font, WHITE, WIDTH // 2, HEIGHT // 2)
        draw_text("Press SPACE to Restart", font, WHITE, WIDTH // 2, HEIGHT // 2 + 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

# Main flow
while True:
    start_screen()
    final_score = game_loop()
    game_over_screen(final_score)
