import pygame
import tkinter as tk
from tkinter import messagebox

# Initialize the Tkinter window
root = tk.Tk()
root.title("Shooting Game Menu")
root.geometry("400x300")
root.configure(bg='black')

# Variable to store the game mode and difficulty
game_mode = tk.StringVar()
difficulty = tk.StringVar(value='Normal')

def main_menu():
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    # Configure window
    root.title("Shooting Game Menu")
    root.geometry("400x300")
    root.configure(bg='black')

    # Create buttons for game modes
    local_button = tk.Button(root, text="Play Locally", width=20, command=lambda: start_game('local'),
                             bg='gray', fg='white', activebackground='lightgray', activeforeground='black')
    ai_button = tk.Button(root, text="Play Against AI", width=20, command=ai_menu,
                          bg='gray', fg='white', activebackground='lightgray', activeforeground='black')
    exit_button = tk.Button(root, text="Exit", width=20, command=root.quit,
                            bg='gray', fg='white', activebackground='lightgray', activeforeground='black')

    local_button.pack(pady=20)
    ai_button.pack(pady=20)
    exit_button.pack(pady=20)

def ai_menu():
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    # Configure window
    root.title("Select Difficulty")
    root.geometry("400x300")
    root.configure(bg='black')

    # Difficulty options
    difficulties = ['Easy', 'Normal', 'Hard']

    def set_difficulty(diff):
        global difficulty
        difficulty = diff
        start_game('ai')

    # Create buttons for difficulty levels
    for diff in difficulties:
        diff_button = tk.Button(root, text=diff, width=20, command=lambda d=diff: set_difficulty(d),
                                bg='gray', fg='white', activebackground='lightgray', activeforeground='black')
        diff_button.pack(pady=10)

    back_button = tk.Button(root, text="Back", width=20, command=main_menu,
                            bg='gray', fg='white', activebackground='lightgray', activeforeground='black')
    back_button.pack(pady=20)

main_menu()
root.mainloop()

def main_game():
    # Initialize Pygame
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Fun Shooting Game")

    # Define colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    GRAY = (100, 100, 100)
    LIGHT_GRAY = (170, 170, 170)

    # Player class
    class Player(pygame.sprite.Sprite):
        def __init__(self, color, x, y, controls=None):
            super().__init__()
            self.image = pygame.Surface((50, 50))
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.speed = 5
            self.controls = controls
            self.health = 100
            self.last_shot_time = 0  # For shooting cooldown

        def update(self):
            keys = pygame.key.get_pressed()
            if self.controls:
                if keys[self.controls['left']]:
                    self.rect.x -= self.speed
                if keys[self.controls['right']]:
                    self.rect.x += self.speed
                if keys[self.controls['up']]:
                    self.rect.y -= self.speed
                if keys[self.controls['down']]:
                    self.rect.y += self.speed

                # Keep player on screen
                if self.rect.left < 0:
                    self.rect.left = 0
                if self.rect.right > screen_width:
                    self.rect.right = screen_width
                if self.rect.top < 0:
                    self.rect.top = 0
                if self.rect.bottom > screen_height:
                    self.rect.bottom = screen_height

    # Bullet class
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y, dx, dy, color, owner):
            super().__init__()
            self.image = pygame.Surface((10, 10))
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.dx = dx
            self.dy = dy
            self.owner = owner  # Reference to the player who fired the bullet

        def update(self):
            self.rect.x += self.dx
            self.rect.y += self.dy
            if (self.rect.x < 0 or self.rect.x > screen_width or
                self.rect.y < 0 or self.rect.y > screen_height):
                self.kill()

    def create_players():
        # Create player instances
        player1_controls = {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w,
                            'down': pygame.K_s, 'shoot': pygame.K_SPACE}
        player1 = Player(RED, 100, screen_height // 2, controls=player1_controls)

        if game_mode == 'local':
            player2_controls = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
                                'up': pygame.K_UP, 'down': pygame.K_DOWN, 'shoot': pygame.K_RETURN}
            player2 = Player(BLUE, screen_width - 100, screen_height // 2, controls=player2_controls)
            is_ai = False
        else:
            player2 = Player(BLUE, screen_width - 100, screen_height // 2)  # AI player
            is_ai = True

        return player1, player2, is_ai

    # Initialize players and game variables
    player1, player2, is_ai = create_players()

    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    players = pygame.sprite.Group()

    all_sprites.add(player1, player2)
    players.add(player1, player2)

    clock = pygame.time.Clock()

    game_over = False  # Flag to indicate game over
    winner = None      # Variable to store the winner

    # Difficulty settings
    ai_shoot_interval = 1000  # Default is 'Normal' difficulty
    ai_speed = 5

    if difficulty == 'Easy':
        ai_shoot_interval = 1500
        ai_speed = 3
    elif difficulty == 'Hard':
        ai_shoot_interval = 700
        ai_speed = 7

    # Game loop
    running = True
    while running:
        dt = clock.tick(60)  # Limit to 60 FPS and get delta time in milliseconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle mouse click on buttons
            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if new_game_button.collidepoint(mouse_pos):
                    # Reset game state
                    player1, player2, is_ai = create_players()
                    all_sprites.empty()
                    bullets.empty()
                    players.empty()
                    all_sprites.add(player1, player2)
                    players.add(player1, player2)
                    game_over = False
                    winner = None
                elif main_menu_button.collidepoint(mouse_pos):
                    # Return to main menu
                    running = False
                    pygame.quit()
                    # Restart the Tkinter main menu
                    root = tk.Tk()
                    main_menu()
                    root.mainloop()
                    main_game()  # Start the game again after menu
                    return  # Exit the current game loop

        if not game_over:
            # Player shooting with cooldown
            keys = pygame.key.get_pressed()
            current_time = pygame.time.get_ticks()

            # Player 1 shooting
            if keys[player1_controls['shoot']]:
                if current_time - player1.last_shot_time > 500:  # 500 ms cooldown
                    bullet = Bullet(player1.rect.centerx, player1.rect.centery, 10, 0, RED, owner=player1)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    player1.last_shot_time = current_time

            # Player 2 shooting
            if not is_ai:
                if keys[player2_controls['shoot']]:
                    if current_time - player2.last_shot_time > 500:  # 500 ms cooldown
                        bullet = Bullet(player2.rect.centerx, player2.rect.centery, -10, 0, BLUE, owner=player2)
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                        player2.last_shot_time = current_time

            # AI behavior
            if is_ai:
                # Simple AI: move towards player1 and shoot
                if player2.rect.y < player1.rect.y:
                    player2.rect.y += ai_speed
                if player2.rect.y > player1.rect.y:
                    player2.rect.y -= ai_speed

                # Keep AI on screen
                if player2.rect.top < 0:
                    player2.rect.top = 0
                if player2.rect.bottom > screen_height:
                    player2.rect.bottom = screen_height

                # AI shooting with cooldown
                if current_time - player2.last_shot_time > ai_shoot_interval:
                    bullet = Bullet(player2.rect.centerx, player2.rect.centery, -10, 0, BLUE, owner=player2)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    player2.last_shot_time = current_time

            # Update all sprites
            all_sprites.update()

            # Check for bullet collisions
            for bullet in bullets:
                # Check collision with players other than the owner
                hit_players = pygame.sprite.spritecollide(bullet, players, False)
                for hit_player in hit_players:
                    if hit_player != bullet.owner:
                        hit_player.health -= 10
                        bullet.kill()

            # Check for game over
            if player1.health <= 0 or player2.health <= 0:
                winner = "Player 1" if player2.health <= 0 else "Player 2"
                game_over = True

        # Draw everything
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Display health
        font = pygame.font.Font(None, 36)
        health_text1 = font.render(f"P1 Health: {player1.health}", True, WHITE)
        health_text2 = font.render(f"P2 Health: {player2.health}", True, WHITE)
        screen.blit(health_text1, (10, 10))
        screen.blit(health_text2, (screen_width - health_text2.get_width() - 10, 10))

        if game_over:
            # Display winner text
            font = pygame.font.Font(None, 74)
            text = font.render(f"{winner} Wins!", True, WHITE)
            screen.blit(text, (screen_width // 2 - text.get_width() // 2,
                               screen_height // 2 - text.get_height() // 2 - 100))

            # Draw "New Game" button
            button_width = 200
            button_height = 50

            new_game_button = pygame.Rect(screen_width // 2 - button_width // 2,
                                          screen_height // 2 - button_height // 2,
                                          button_width, button_height)
            pygame.draw.rect(screen, LIGHT_GRAY, new_game_button)
            pygame.draw.rect(screen, WHITE, new_game_button, 2)  # Border

            # Button text
            button_font = pygame.font.Font(None, 48)
            button_text = button_font.render("New Game", True, BLACK)
            screen.blit(button_text, (new_game_button.x + (button_width - button_text.get_width()) // 2,
                                      new_game_button.y + (button_height - button_text.get_height()) // 2))

            # Draw "Main Menu" button
            main_menu_button = pygame.Rect(screen_width // 2 - button_width // 2,
                                           screen_height // 2 + button_height,
                                           button_width, button_height)
            pygame.draw.rect(screen, LIGHT_GRAY, main_menu_button)
            pygame.draw.rect(screen, WHITE, main_menu_button, 2)  # Border

            # Button text
            main_menu_text = button_font.render("Main Menu", True, BLACK)
            screen.blit(main_menu_text, (main_menu_button.x + (button_width - main_menu_text.get_width()) // 2,
                                         main_menu_button.y + (button_height - main_menu_text.get_height()) // 2))

        pygame.display.flip()

    pygame.quit()

def start_game(mode):
    global game_mode
    game_mode = mode
    root.destroy()  # Close the menu window
    main_game()     # Start the pygame window

# Start the main menu when the script is run
if __name__ == "__main__":
    main_menu()
