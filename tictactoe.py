import tkinter as tk
from tkinter import messagebox
import random

class Game:
    def __init__(self):
        self.levels = [Level(1), Level(2), Level(3)]
        self.current_level_index = 0
        self.current_level = self.levels[self.current_level_index]
        self.board = Board()
        self.player_x = HumanPlayer("X")
        self.player_o = AIPlayer("O", self.current_level.difficulty)
        self.current_player = self.player_x
        self.interface = None  # Initialize with None, to be set later
        self.game_logic = GameLogic()

    def set_interface(self, interface):
        self.interface = interface

    def next_level(self):
        self.current_level_index += 1
        if self.current_level_index < len(self.levels):
            self.current_level = self.levels[self.current_level_index]
            self.player_o.difficulty = self.current_level.difficulty
            self.board.reset()
            self.interface.reset_board()
        else:
            messagebox.showinfo("Game Over", "You've completed all levels!")
            self.interface.window.quit()

    def switch_player(self):
        self.current_player = self.player_o if self.current_player == self.player_x else self.player_x

    def play_turn(self, row, col):
        if self.board.is_empty(row, col):
            self.board.update_board(row, col, self.current_player.symbol)
            self.interface.update_button(row, col, self.current_player.symbol)
            if self.game_logic.check_winner(self.board, self.current_player.symbol):
                messagebox.showinfo("Game Over", f"Player {self.current_player.symbol} wins!")
                self.next_level()
            elif self.board.is_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.next_level()
            else:
                self.switch_player()
                if isinstance(self.current_player, AIPlayer):
                    self.play_ai_turn()

    def play_ai_turn(self):
        row, col = self.current_player.get_move(self.board)
        self.play_turn(row, col)

class Level:
    def __init__(self, number):
        self.number = number
        self.difficulty = ["Easy", "Medium", "Hard"][number - 1]

class Board:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]

    def update_board(self, row, col, symbol):
        self.board[row][col] = symbol

    def is_empty(self, row, col):
        return self.board[row][col] == ""

    def is_full(self):
        return all(all(cell != "" for cell in row) for row in self.board)

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

class HumanPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)

class AIPlayer(Player):
    def __init__(self, symbol, difficulty):
        super().__init__(symbol)
        self.difficulty = difficulty

    def get_move(self, board):
        if self.difficulty == "Easy":
            return self.random_move(board)
        elif self.difficulty == "Medium":
            return self.blocking_move(board) or self.random_move(board)
        elif self.difficulty == "Hard":
            return self.winning_move(board) or self.blocking_move(board) or self.random_move(board)

    def random_move(self, board):
        empty_cells = [(r, c) for r in range(3) for c in range(3) if board.is_empty(r, c)]
        return random.choice(empty_cells)

    def blocking_move(self, board):
        opponent_symbol = "X" if self.symbol == "O" else "O"
        return self.find_winning_move(board, opponent_symbol)

    def winning_move(self, board):
        return self.find_winning_move(board, self.symbol)

    def find_winning_move(self, board, symbol):
        for r in range(3):
            for c in range(3):
                if board.is_empty(r, c):
                    board.update_board(r, c, symbol)
                    if GameLogic().check_winner(board, symbol):
                        board.update_board(r, c, "")
                        return (r, c)
                    board.update_board(r, c, "")
        return None

class GameInterface:
    def __init__(self, game):
        self.game = game
        self.game.set_interface(self)  # Set the interface reference in the game
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.buttons = [[tk.Button(self.window, text="", width=10, height=3, command=lambda r=r, c=c: self.on_click(r, c)) for c in range(3)] for r in range(3)]
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].grid(row=r, column=c)
        self.reset_button = tk.Button(self.window, text="Reset", command=self.reset_board)
        self.reset_button.grid(row=3, column=0, columnspan=3)
        self.window.mainloop()

    def on_click(self, row, col):
        self.game.play_turn(row, col)

    def update_button(self, row, col, symbol):
        self.buttons[row][col].config(text=symbol, state=tk.DISABLED)

    def reset_board(self):
        for row in self.buttons:
            for button in row:
                button.config(text="", state=tk.NORMAL)
        self.game.board.reset()

class GameLogic:
    def check_winner(self, board, symbol):
        b = board.board
        for i in range(3):
            if all(b[i][j] == symbol for j in range(3)) or all(b[j][i] == symbol for j in range(3)):
                return True
        if b[0][0] == b[1][1] == b[2][2] == symbol or b[0][2] == b[1][1] == b[2][0] == symbol:
            return True
        return False

if __name__ == "__main__":
    game = Game()
    interface = GameInterface(game)
