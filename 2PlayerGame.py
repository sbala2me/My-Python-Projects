import tkinter as tk
import random

class Player:
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(x, y, x + 50, y + 60, fill=color)
        self.health = 100

    def move(self, dx, dy):
        self.canvas.move(self.id, dx, dy)

    def get_position(self):
        return self.canvas.coords(self.id)

    def attack(self, opponent):
        my_coords = self.get_position()
        opp_coords = opponent.get_position()
        # Check if players are colliding
        if (my_coords[0] < opp_coords[2] and my_coords[2] > opp_coords[0] and
            my_coords[1] < opp_coords[3] and my_coords[3] > opp_coords[1]):
            opponent.health -= 5

class FightingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("2 Player Fighting Game")
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()

        self.player1 = Player(self.canvas, 100, 300, "red")
        self.player2 = Player(self.canvas, 600, 300, "blue")

        self.setup_controls()
        self.ai_mode = False  # Set to True for AI vs Player

        self.update_health()
        self.run_game()

    def setup_controls(self):
        self.root.bind("w", lambda event: self.player1.move(0, -10))
        self.root.bind("s", lambda event: self.player1.move(0, 10))
        self.root.bind("a", lambda event: self.player1.move(-10, 0))
        self.root.bind("d", lambda event: self.player1.move(10, 0))
        self.root.bind("<space>", lambda event: self.player1.attack(self.player2))

        self.root.bind("<Up>", lambda event: self.player2.move(0, -10))
        self.root.bind("<Down>", lambda event: self.player2.move(0, 10))
        self.root.bind("<Left>", lambda event: self.player2.move(-10, 0))
        self.root.bind("<Right>", lambda event: self.player2.move(10, 0))
        self.root.bind("<Return>", lambda event: self.player2.attack(self.player1))

    def update_health(self):
        self.canvas.delete("health")
        self.canvas.create_text(150, 50, text=f"Player 1 Health: {self.player1.health}", tag="health", fill="red", font=("Arial", 14))
        self.canvas.create_text(650, 50, text=f"Player 2 Health: {self.player2.health}", tag="health", fill="blue", font=("Arial", 14))

    def ai_movement(self):
        p2_coords = self.player2.get_position()
        p1_coords = self.player1.get_position()

        # Basic AI movement towards Player 1
        if p2_coords[0] < p1_coords[0]:
            self.player2.move(5, 0)
        elif p2_coords[0] > p1_coords[0]:
            self.player2.move(-5, 0)
        if p2_coords[1] < p1_coords[1]:
            self.player2.move(0, 5)
        elif p2_coords[1] > p1_coords[1]:
            self.player2.move(0, -5)

        # AI Attack randomly when close to Player 1
        if random.randint(0, 10) == 0:
            self.player2.attack(self.player1)

    def check_winner(self):
        if self.player1.health <= 0:
            self.canvas.create_text(400, 300, text="Player 2 Wins!", fill="blue", font=("Arial", 24))
            return True
        if self.player2.health <= 0:
            self.canvas.create_text(400, 300, text="Player 1 Wins!", fill="red", font=("Arial", 24))
            return True
        return False

    def run_game(self):
        if not self.check_winner():
            if self.ai_mode:
                self.ai_movement()

            self.update_health()
            self.root.after(50, self.run_game)

# Create the main window and run the game
root = tk.Tk()
game = FightingGame(root)
root.mainloop()
