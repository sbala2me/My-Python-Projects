import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2 Player Fighting Game")

# Define Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Define Player Class
class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 60
        self.color = color
        self.velocity = 5
        self.health = 100

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def attack(self, other_player):
        if self.x < other_player.x + other_player.width and \
           self.x + self.width > other_player.x and \
           self.y < other_player.y + other_player.height and \
           self.y + self.height > other_player.y:
            other_player.health -= 5

# Create Players
player1 = Player(100, 300, RED)
player2 = Player(600, 300, BLUE)

# Define AI behavior
def ai_movement(player, opponent):
    if player.x < opponent.x:
        player.x += player.velocity
    elif player.x > opponent.x:
        player.x -= player.velocity
    if player.y < opponent.y:
        player.y += player.velocity
    elif player.y > opponent.y:
        player.y -= player.velocity

# Main Game Loop
def main():
    run_game = True
    two_player_mode = True  # Change this to False to play against AI

    while run_game:
        clock.tick(FPS)
        screen.fill(WHITE)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False

        # Player Movements (Local Play or Player vs AI)
        keys = pygame.key.get_pressed()
        
        # Player 1 Controls
        if keys[pygame.K_a] and player1.x - player1.velocity > 0:  # Left
            player1.x -= player1.velocity
        if keys[pygame.K_d] and player1.x + player1.width + player1.velocity < WIDTH:  # Right
            player1.x += player1.velocity
        if keys[pygame.K_w] and player1.y - player1.velocity > 0:  # Up
            player1.y -= player1.velocity
        if keys[pygame.K_s] and player1.y + player1.height + player1.velocity < HEIGHT:  # Down
            player1.y += player1.velocity
        if keys[pygame.K_SPACE]:  # Attack
            player1.attack(player2)

        # Player 2 Controls or AI
        if two_player_mode:
            if keys[pygame.K_LEFT] and player2.x - player2.velocity > 0:  # Left
                player2.x -= player2.velocity
            if keys[pygame.K_RIGHT] and player2.x + player2.width + player2.velocity < WIDTH:  # Right
                player2.x += player2.velocity
            if keys[pygame.K_UP] and player2.y - player2.velocity > 0:  # Up
                player2.y -= player2.velocity
            if keys[pygame.K_DOWN] and player2.y + player2.height + player2.velocity < HEIGHT:  # Down
                player2.y += player2.velocity
            if keys[pygame.K_RETURN]:  # Attack
                player2.attack(player1)
        else:
            ai_movement(player2, player1)
            if random.randint(0, 60) == 0:  # AI Random Attack
                player2.attack(player1)

        # Draw Players
        player1.draw(screen)
        player2.draw(screen)

        # Display Health
        pygame.draw.rect(screen, RED, (50, 50, player1.health * 2, 20))
        pygame.draw.rect(screen, BLUE, (WIDTH - 250, 50, player2.health * 2, 20))

        # Check for Winner
        if player1.health <= 0:
            print("Player 2 Wins!" if two_player_mode else "AI Wins!")
            run_game = False
        if player2.health <= 0:
            print("Player 1 Wins!")
            run_game = False

        # Update Display
        pygame.display.update()

    pygame.quit()

# Run the Game
if __name__ == "__main__":
    main()
