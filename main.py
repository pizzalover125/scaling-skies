import pygame
from random import randint
import sys

# Initialize constants
WIDTH = 400
HEIGHT = 600
SKY = (135, 206, 235)
GRASS = (0, 128, 0)
FPS = 45

# Initialize pygame
pygame.init()
canvas = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scaling Skies")
clock = pygame.time.Clock()

# Load images
cloud_image = pygame.image.load("cloud.png")
spaceship_image = pygame.image.load("spaceship.png").convert_alpha()
logo_image = pygame.image.load("logo.png").convert_alpha()

# Scale the spaceship image to your desired dimensions
spaceship_image = pygame.transform.scale(spaceship_image, (50, 50))

# Calculate the center of the window
center_x = WIDTH // 2
center_y = HEIGHT // 2

# Calculate the top-left corner of the logo image
logo_x = center_x - (logo_image.get_width() // 2)

# Player variables
player_x = (WIDTH // 2) - 25
player_y = HEIGHT - 100
player_width = 50
player_height = 50

# Score
score = 0
font = pygame.font.Font("Rubik.ttf", 48)


# Function to generate random cloud widths
def cloud_width():
    rect1w = randint(25, 275)
    rect2w = 325 - rect1w
    return [rect1w, rect2w]


# Initialize cloud widths
widths = cloud_width()

# Initialize the game state
game_over = False
start_screen = True
cloud_y = 0
cloud_speed = 5
green_box_height = 50

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()

    # Show the start screen
    if start_screen:
        canvas.fill(SKY)
        pygame.draw.rect(canvas, GRASS, (0, HEIGHT - 50, WIDTH, 50))
        canvas.blit(spaceship_image, (player_x, player_y))

        canvas.blit(logo_image, (logo_x, 0))

        start_text = font.render("Space to start", True, (0, 0, 0))
        text_rect = start_text.get_rect(center=(center_x, center_y))
        canvas.blit(start_text, text_rect)

        pygame.display.update()

        if keys[pygame.K_SPACE]:
            start_screen = False

    # Game is running
    else:
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= 7
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += 7

        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        cloud_rect1 = pygame.Rect(0, cloud_y, widths[0], 100)
        cloud_rect2 = pygame.Rect(WIDTH - widths[1], cloud_y, widths[1], 100)

        if player_rect.colliderect(cloud_rect1) or player_rect.colliderect(cloud_rect2):
            game_over = True

        canvas.fill(SKY)

        cloud_image1 = pygame.transform.scale(cloud_image, (widths[0], 100))
        canvas.blit(cloud_image1, (0, cloud_y))

        cloud_image2 = pygame.transform.scale(cloud_image, (widths[1], 100))
        canvas.blit(cloud_image2, (WIDTH - widths[1], cloud_y))

        canvas.blit(spaceship_image, (player_x, player_y))

        pygame.draw.rect(
            canvas, GRASS, (0, HEIGHT - green_box_height, WIDTH, green_box_height)
        )
        green_box_height -= cloud_speed

        score_text = font.render(f"{score}m", True, (0, 0, 0))
        canvas.blit(score_text, (10, 10))

        cloud_y += cloud_speed

        if cloud_y > HEIGHT:
            cloud_y = -50
            if cloud_speed < 8:
                cloud_speed *= 1.05

            widths = cloud_width()

        score += 1

        pygame.display.update()

        clock.tick(FPS)

pygame.quit()
sys.exit()
