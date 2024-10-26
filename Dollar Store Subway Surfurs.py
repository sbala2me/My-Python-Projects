import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Runner Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)

# Game Variables
LANE_WIDTH = WIDTH // 3
player_pos = 1  # Start in the middle lane
player_y = HEIGHT - 100
player_size = 50
player_speed = 5
obstacle_speed = 10

# Object settings
obstacles = []
coins = []
score = 0

# Fonts
font = pygame.font.SysFont(None, 40)

# Helper Functions
def spawn_obstacle():
    lane = random.randint(0, 2)  # Randomly choose one of three lanes
    x_pos = LANE_WIDTH * lane + LANE_WIDTH // 2 - player_size // 2
    obstacles.append(pygame.Rect(x_pos, -100, player_size, player_size))

def spawn_coin():
    lane = random.randint(0, 2)
    x_pos = LANE_WIDTH * lane + LANE_WIDTH // 2 - player_size // 2
    coins.append(pygame.Rect(x_pos, -100, player_size // 2, player_size // 2))

# Game loop
clock = pygame.time.Clock()
running = True
spawn_timer = 0

while running:
    screen.fill(GRAY)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player_pos > 0:
                player_pos -= 1  # Move left
            elif event.key == pygame.K_RIGHT and player_pos < 2:
                player_pos += 1  # Move right

    # Update Player Position
    player_x = LANE_WIDTH * player_pos + LANE_WIDTH // 2 - player_size // 2
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    pygame.draw.rect(screen, GREEN, player_rect)

    # Spawn Obstacles and Coins
    spawn_timer += 1
    if spawn_timer >= 30:  # Spawn every half second or so
        spawn_obstacle()
        if random.random() < 0.5:  # 50% chance to spawn a coin
            spawn_coin()
        spawn_timer = 0

    # Update and Draw Obstacles
    for obstacle in obstacles[:]:
        obstacle.y += obstacle_speed
        pygame.draw.rect(screen, RED, obstacle)
        if obstacle.colliderect(player_rect):
            print("Collision! Game Over!")
            pygame.quit()
            sys.exit()
        if obstacle.y > HEIGHT:
            obstacles.remove(obstacle)

    # Update and Draw Coins
    for coin in coins[:]:
        coin.y += obstacle_speed
        pygame.draw.circle(screen, YELLOW, (coin.x + player_size // 4, coin.y + player_size // 4), player_size // 4)
        if coin.colliderect(player_rect):
            score += 1  # Collect coin and increase score
            coins.remove(coin)
        if coin.y > HEIGHT:
            coins.remove(coin)

    # Display Score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
