import tkinter as tk
import random

class Player:
    def __init__(self, canvas: tk.Canvas, x: int, y: int, color: str):
        """
        Initializes the player with position and color.
        """
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(x, y, x + 50, y + 60, fill=color)
        self.health = 100

    def move(self, dx: int, dy: int) -> None:
        """
        Moves the player by dx and dy on the canvas.
        """
        self.canvas.move(self.id, dx, dy)

    def get_position(self) -> list:
        """
        Returns the current coordinates of the player.
        """
        return self.canvas.coords(self.id)

    def attack(self, opponent: "Player") -> None:
        """
        Checks collision with the opponent and reduces opponent's health.
        """
        if self._is_colliding(opponent):
            opponent.health -= 5

    def _is_colliding(self, opponent: "Player") -> bool:
        """
        Determines if the player is colliding with the opponent.
        """
        my_coords = self.get_position()
        opp_coords = opponent.get_position()
        return (my_coords and opp_coords and  # Check if the coordinates are not empty
                my_coords[0] < opp_coords[2] and my_coords[2] > opp_coords[0] and
                my_coords[1] < opp_coords[3] and my_coords[3] > opp_coords[1])

class FightingGame:
    AI_ATTACK_CHANCE = 10  # The lower the number, the higher the chance to attack
    MOVE_STEP = 10

    def __init__(self, root: tk.Tk):
        """
        Initializes the game window, players, controls, and the new game button.
        """
        self.root = root
        self.root.title("2 Player Fighting Game")
        
        # Create the main menu
        self.main_menu_frame = tk.Frame(root, bg="black")
        self.main_menu_frame.pack(fill="both", expand=True)

        title_label = tk.Label(self.main_menu_frame, text="2 Player Fighting Game", 
                               font=("Arial", 30), bg="black", fg="white")
        title_label.pack(pady=100)

        start_button = tk.Button(self.main_menu_frame, text="Start Game", font=("Arial", 20),
                                 command=self.start_game)
        start_button.pack(pady=20)

        ai_button = tk.Button(self.main_menu_frame, text="Play Against AI", font=("Arial", 20),
                              command=self.start_game_with_ai)
        ai_button.pack(pady=20)

        self.canvas = tk.Canvas(root, width=800, height=600, bg="black")

    def start_game(self) -> None:
        """
        Starts the game by switching from the main menu to the game screen.
        """
        self.ai_mode = False  # Default to player vs player mode
        self._start_game_screen()

    def start_game_with_ai(self) -> None:
        """
        Starts the game with AI by switching from the main menu to the game screen.
        """
        self.ai_mode = True
        self._start_game_screen()

    def _start_game_screen(self) -> None:
        """
        Configures the game screen and sets up players.
        """
        self.main_menu_frame.pack_forget()  # Hide the main menu frame
        self.canvas.pack()  # Display the game canvas

        self.new_game_button = tk.Button(self.root, text="New Game", command=self.new_game)
        self.new_game_button.pack()

        self.player1 = Player(self.canvas, 100, 300, "red")
        self.player2 = Player(self.canvas, 600, 300, "blue")

        self._setup_controls()
        self._start_game()

    def _setup_controls(self) -> None:
        """
        Configures key bindings for player movements and attacks.
        """
        self.root.bind("w", lambda event: self.player1.move(0, -self.MOVE_STEP))
        self.root.bind("s", lambda event: self.player1.move(0, self.MOVE_STEP))
        self.root.bind("a", lambda event: self.player1.move(-self.MOVE_STEP, 0))
        self.root.bind("d", lambda event: self.player1.move(self.MOVE_STEP, 0))
        self.root.bind("<space>", lambda event: self.player1.attack(self.player2))

        if not self.ai_mode:  # Player 2 controls only if AI mode is off
            self.root.bind("<Up>", lambda event: self.player2.move(0, -self.MOVE_STEP))
            self.root.bind("<Down>", lambda event: self.player2.move(0, self.MOVE_STEP))
            self.root.bind("<Left>", lambda event: self.player2.move(-self.MOVE_STEP, 0))
            self.root.bind("<Right>", lambda event: self.player2.move(self.MOVE_STEP, 0))
            self.root.bind("<Return>", lambda event: self.player2.attack(self.player1))

    def _update_health_display(self) -> None:
        """
        Updates the health display on the canvas.
        """
        self.canvas.delete("health")
        self.canvas.create_text(150, 50, text=f"Player 1 Health: {self.player1.health}", 
                                tag="health", fill="red", font=("Arial", 14))
        self.canvas.create_text(650, 50, text=f"Player 2 Health: {self.player2.health}", 
                                tag="health", fill="blue", font=("Arial", 14))

    def _ai_movement(self) -> None:
        """
        Controls the basic AI movement and attacks for player 2.
        """
        p2_coords = self.player2.get_position()
        p1_coords = self.player1.get_position()

        # Basic AI movement towards Player 1
        dx = 5 if p2_coords[0] < p1_coords[0] else -5 if p2_coords[0] > p1_coords[0] else 0
        dy = 5 if p2_coords[1] < p1_coords[1] else -5 if p2_coords[1] > p1_coords[1] else 0
        self.player2.move(dx, dy)

        # AI Attack randomly when close to Player 1
        if random.randint(0, self.AI_ATTACK_CHANCE) == 0:
            self.player2.attack(self.player1)

    def _check_winner(self) -> bool:
        """
        Checks if any player has won and displays the result.
        """
        if self.player1.health <= 0:
            self._display_winner("Player 2 Wins!", "blue")
            return True
        if self.player2.health <= 0:
            self._display_winner("Player 1 Wins!", "red")
            return True
        return False

    def _display_winner(self, message: str, color: str) -> None:
        """
        Displays the winner message on the canvas.
        """
        self.canvas.create_text(400, 300, text=message, fill=color, font=("Arial", 24))

    def _start_game(self) -> None:
        """
        Initiates the game loop.
        """
        if not self._check_winner():
            if self.ai_mode:
                self._ai_movement()

            self._update_health_display()
            self.root.after(50, self._start_game)

    def new_game(self) -> None:
        """
        Resets the game to its initial state and returns to the main menu.
        """
        # Hide the canvas and the "New Game" button
        self.canvas.pack_forget()
        self.new_game_button.pack_forget()

        # Clear the canvas of all elements
        self.canvas.delete("all")

        # Show the main menu again
        self.main_menu_frame.pack(fill="both", expand=True)

# Create the main window and run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = FightingGame(root)
    root.mainloop()
