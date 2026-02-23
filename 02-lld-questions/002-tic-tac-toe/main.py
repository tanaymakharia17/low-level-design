
"""
Flow:
2 players are created
Start a new tictac board game
each player alternatively play
check after each move of who won
after winning print winning player and reset board

Possible classes:
MoveType (o, x)
Player(name, id, age, MoveTypeAssigned)
PlayerFactory() - No
Board
BoardFactory() - No

TictacToeController


"""
from enum import Enum

class MoveType(Enum):
    ZERO = 1
    CROSS = 2

class CellState(MoveType):
    EMPTY = 3

class Player:
    def __init__(self, id, name, move_type: MoveType):
        self.id = id
        self.name = name
        self.move = move_type

class Board:
    def __init__(self):
        self._board = []
        for i in range(3):
            self._board.append([CellState.EMPTY]*3)


class TictacToeController:

    def __init__(self, board, player1, player2):
        self.board = board
        self.player1 = player1
        self.player2 = player2



player1 = Player(1, "Tanay", MoveType.ZERO)
player2 = Player(1, "Tanay", MoveType.CROSS)
board = Board()

controller = TictacToeController(board, player1, player2)

#---------------------------------------------------------------------------------------------------------------
from enum import Enum
from typing import List, Optional


class MoveType(Enum):
    X = "X"
    O = "O"


class CellState(Enum):
    EMPTY = "-"
    X = "X"
    O = "O"


class Player:
    def __init__(self, player_id: int, name: str, move: MoveType):
        self.id = player_id
        self.name = name
        self.move = move

    def __str__(self):
        return f"{self.name} ({self.move.value})"


class Board:
    def __init__(self, size: int = 3):
        self.size = size
        self.grid: List[List[CellState]] = [
            [CellState.EMPTY for _ in range(size)] for _ in range(size)
        ]

    def display(self):
        for row in self.grid:
            print(" | ".join(cell.value for cell in row))
        print()

    def is_valid_move(self, row: int, col: int) -> bool:
        return (
            0 <= row < self.size
            and 0 <= col < self.size
            and self.grid[row][col] == CellState.EMPTY
        )

    def make_move(self, row: int, col: int, move: MoveType) -> bool:
        if self.is_valid_move(row, col):
            self.grid[row][col] = CellState[move.name]
            return True
        return False

    def check_winner(self) -> Optional[MoveType]:
        lines = []

        for i in range(self.size):
            lines.append(self.grid[i])  # row
            lines.append([self.grid[j][i] for j in range(self.size)])  # column

        lines.append([self.grid[i][i] for i in range(self.size)])  # diagonal
        lines.append([self.grid[i][self.size - 1 - i] for i in range(self.size)])  # anti-diagonal

        for line in lines:
            if all(cell == CellState.X for cell in line):
                return MoveType.X
            if all(cell == CellState.O for cell in line):
                return MoveType.O

        return None

    def is_full(self) -> bool:
        return all(cell != CellState.EMPTY for row in self.grid for cell in row)


class Game:
    def __init__(self, player1: Player, player2: Player):
        if player1.move == player2.move:
            raise ValueError("Players must have different symbols.")
        self.board = Board()
        self.players = [player1, player2]
        self.current_index = 0

    def start(self):
        print(f"Starting Tic Tac Toe between {self.players[0]} and {self.players[1]}")
        self.board.display()

        while True:
            current_player = self.players[self.current_index]
            print(f"{current_player}'s turn")

            try:
                row = int(input("Enter row (0-2): "))
                col = int(input("Enter col (0-2): "))
            except ValueError:
                print("Please enter valid integers.")
                continue

            if not self.board.make_move(row, col, current_player.move):
                print("Invalid move. Try again.")
                continue

            self.board.display()

            winner = self.board.check_winner()
            if winner:
                print(f"{current_player} wins!")
                break

            if self.board.is_full():
                print("It's a draw!")
                break

            self.current_index = 1 - self.current_index
