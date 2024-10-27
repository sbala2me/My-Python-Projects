import pygame

# Game variables
WIDTH, HEIGHT = 800, 600
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
PLAYER_SPEED = 5
MAX_BULLETS = 5
MAX_HEALTH = 100

# Initialize Pygame
pygame.init()

# Game window setup
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Two-Player Shooting Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Guns with attributes
guns = {
    "Pistol": {"bullet_speed": 5, "damage": 1, "color": WHITE},
    "Rifle": {"bullet_speed": 7, "damage": 2, "color": GREEN},
    "Sniper": {"bullet_speed": 10, "damage": 5, "color": RED},
    "Shotgun": {"bullet_speed": 4, "damage": 1.5, "color": BLUE, "spread": True},
    "RPG": {"bullet_speed": 3, "damage": 7, "color": ORANGE},
    "Machine Gun": {"bullet_speed": 8, "damage": 0.5, "color": PURPLE},
    "Laser Gun": {"bullet_speed": 12, "damage": 2.5, "color": CYAN},
    "Knife": {"bullet_speed": 0, "damage": 8, "color": YELLOW, "melee": True}
}

# Player selections
player1_gun = None
player2_gun = None

# Game state variables
choosing_guns = True
game_over = False
fullscreen = False
winner_text = ""

# Health
player1_health = MAX_HEALTH
player2_health = MAX_HEALTH


# Initialize player positions and bullets
def create_players():
    player1 = pygame.Rect(100, HEIGHT // 2 - PLAYER_WIDTH // 2, PLAYER_WIDTH, PLAYER_HEIGHT)
    player2 = pygame.Rect(WIDTH - 150, HEIGHT // 2 - PLAYER_WIDTH // 2, PLAYER_WIDTH, PLAYER_HEIGHT)
    return player1, player2


player1, player2 = create_players()
player1_bullets = []
player2_bullets = []


# Reset game state
def reset_game():
    global player1_health, player2_health, player1_bullets, player2_bullets, player1, player2, game_over, choosing_guns, winner_text
    player1_health = MAX_HEALTH
    player2_health = MAX_HEALTH
    player1_bullets = []
    player2_bullets = []
    player1, player2 = create_players()
    game_over = False
    choosing_guns = True
    winner_text = ""


def draw_gun_selection():
    win.fill(BLACK)
    font = pygame.font.Font(None, 36)

    # Display instructions
    instruction_text = font.render("Player 1: Press 1-8 to select a weapon", True, WHITE)
    win.blit(instruction_text, (50, 50))
    instruction_text2 = font.render("Player 2: Press 9-0 to select a weapon", True, WHITE)
    win.blit(instruction_text2, (50, 100))

    # Display gun options
    y_pos = 150
    for i, (gun_name, gun_data) in enumerate(guns.items(), start=1):
        gun_text = font.render(f"{i}. {gun_name} - Speed: {gun_data['bullet_speed']}, Damage: {gun_data['damage']}",
                               True, gun_data["color"])
        win.blit(gun_text, (50, y_pos))
        y_pos += 40

    pygame.display.update()


def handle_movement(keys, player, left, right, up, down):
    if keys[left] and player.x - PLAYER_SPEED > 0:
        player.x -= PLAYER_SPEED
    if keys[right] and player.x + PLAYER_SPEED + player.width < WIDTH:
        player.x += PLAYER_SPEED
    if keys[up] and player.y - PLAYER_SPEED > 0:
        player.y -= PLAYER_SPEED
    if keys[down] and player.y + PLAYER_SPEED + player.height < HEIGHT:
        player.y += PLAYER_SPEED


def handle_bullets(player_bullets, player, opponent, gun):
    global player1_health, player2_health

    # Determine if the gun is melee
    melee = gun.get("melee", False)

    # Handle melee weapon (Knife)
    if melee:
        if player.colliderect(opponent):
            if player == player1:
                player2_health -= gun["damage"]
            else:
                player1_health -= gun["damage"]
        return

    # Handle bullets for ranged weapons
    for bullet in player_bullets:
        bullet.x += gun["bullet_speed"] if player == player1 else -gun["bullet_speed"]

        if opponent.colliderect(bullet):
            player_bullets.remove(bullet)
            if player == player1:
                player2_health -= gun["damage"]
            else:
                player1_health -= gun["damage"]

        elif bullet.x > WIDTH or bullet.x < 0:
            player_bullets.remove(bullet)


def draw_health_bar(health, x, y):
    health_ratio = health / MAX_HEALTH
    pygame.draw.rect(win, RED, (x, y, 100, 10))  # Background health bar
    pygame.draw.rect(win, GREEN, (x, y, 100 * health_ratio, 10))  # Foreground health bar


def draw_window():
    win.fill(BLACK)  # Set background to black

    # Draw players
    pygame.draw.rect(win, RED, player1)
    pygame.draw.rect(win, BLUE, player2)

    # Draw bullets
    for bullet in player1_bullets:
        pygame.draw.rect(win, player1_gun["color"], bullet)
    for bullet in player2_bullets:
        pygame.draw.rect(win, player2_gun["color"], bullet)

    # Draw health bars
    draw_health_bar(player1_health, 10, 10)
    draw_health_bar(player2_health, WIDTH - 110, 10)

    # Display winner message if game is over
    if game_over:
        font = pygame.font.Font(None, 74)
        win_text = font.render(winner_text, True, WHITE)
        win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        win.blit(win_text, win_rect)

    pygame.display.update()


def main_game():
    global player1_health, player2_health, game_over, winner_text, fullscreen, WIDTH, HEIGHT, player1_gun, player2_gun, choosing_guns
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)

        # Gun selection phase
        if choosing_guns:
            draw_gun_selection()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    # Player 1 chooses gun
                    if event.key == pygame.K_1:
                        player1_gun = guns["Pistol"]
                    elif event.key == pygame.K_2:
                        player1_gun = guns["Rifle"]
                    elif event.key == pygame.K_3:
                        player1_gun = guns["Sniper"]
                    elif event.key == pygame.K_4:
                        player1_gun = guns["Shotgun"]
                    elif event.key == pygame.K_5:
                        player1_gun = guns["RPG"]
                    elif event.key == pygame.K_6:
                        player1_gun = guns["Machine Gun"]
                    elif event.key == pygame.K_7:
                        player1_gun = guns["Laser Gun"]
                    elif event.key == pygame.K_8:
                        player1_gun = guns["Knife"]

                    # Player 2 chooses gun
                    elif event.key == pygame.K_9:
                        player2_gun = guns["Pistol"]
                    elif event.key == pygame.K_0:
                        player2_gun = guns["Rifle"]
                    elif event.key == pygame.K_MINUS:
                        player2_gun = guns["Sniper"]
                    elif event.key == pygame.K_EQUALS:
                        player2_gun = guns["Shotgun"]

                    # Start game if both players have selected a gun
                    if player1_gun and player2_gun:
                        choosing_guns = False
            continue

        # Game phase
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # Player 1 shoots with Space
                if event.key == pygame.K_SPACE and len(player1_bullets) < MAX_BULLETS and not player1_gun.get("melee",
                                                                                                              False):
                    bullet = pygame.Rect(player1.x + player1.width, player1.y + player1.height // 2 - 2, 10, 5)
                    player1_bullets.append(bullet)
                # Player 2 shoots with Enter
                if event.key == pygame.K_RETURN and len(player2_bullets) < MAX_BULLETS and not player2_gun.get("melee",
                                                                                                               False):
                    bullet = pygame.Rect(player2.x, player2.y + player2.height // 2 - 2, 10, 5)
                    player2_bullets.append(bullet)

        keys = pygame.key.get_pressed()

        if not game_over:
            handle_movement(keys, player1, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)
            handle_movement(keys, player2, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)

            handle_bullets(player1_bullets, player1, player2, player1_gun)
            handle_bullets(player2_bullets, player2, player1, player2_gun)

            # Check for win condition
            if player1_health <= 0:
                winner_text = "Player 2 Wins!"
                game_over = True
                reset_game()
            elif player2_health <= 0:
                winner_text = "Player 1 Wins!"
                game_over = True
                reset_game()

        draw_window()

    pygame.quit()


# Start the game
reset_game()
main_game()
