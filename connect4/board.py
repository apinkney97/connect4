from __future__ import annotations

from typing import List, Set, Tuple

import colorama
from more_itertools import windowed

# TODO: Maybe convert to curses? https://docs.python.org/3/howto/curses.html
colorama.init()

COLOURS = {
    0: colorama.Style.RESET_ALL,
    1: colorama.Back.RED + colorama.Fore.WHITE,
    2: colorama.Back.BLUE + colorama.Fore.WHITE,
}


Coord = Vector = Tuple[int, int]


class InvalidMoveError(Exception):
    def __init__(self, bad_column: int):
        self.bad_column = bad_column
        super().__init__(f"Can't play in full column {bad_column}")


class Board:
    def __init__(self, width: int = 7, height: int = 6, board=None):
        board_size = width * height
        if board and board_size != len(board):
            raise Exception("Board dimensions don't match provided board data")

        if board:
            self._board = list(board)
        else:
            self._board = [0] * board_size

        self._width = width
        self._height = height

        left_edge = {(0, r) for r in range(self._height)}
        right_edge = {(self._width - 1, r) for r in range(self._height)}
        top_edge = {(c, 0) for c in range(self._width)}

        self._win_lines = [
            (left_edge, (1, 0)),  # rows
            (top_edge, (0, 1)),  # columns
            (left_edge | top_edge, (1, 1)),  # down-right diagonals
            (right_edge | top_edge, (-1, 1)),  # down-left diagonals
        ]

    @classmethod
    def from_nested_board(cls, nested_board: List[List[int]]) -> Board:
        height = len(nested_board)
        width = len(nested_board[0])

        flattened_board = []
        for row in nested_board:
            if len(row) != width:
                raise Exception("Dimensions do not match in supplied nested_board")
            flattened_board += row

        return Board(width=width, height=height, board=flattened_board)

    def __str__(self) -> str:
        lines = [
            "|".join(
                f" {n if self.is_valid_move(n) else ' '} " for n in range(self._width)
            )
        ]
        for row in range(self._height):
            lines.append(
                "|".join(
                    COLOURS[self[col, row]] + "   " + colorama.Style.RESET_ALL
                    for col in range(self._width)
                )
            )
        return ("\n" + "+".join(["---"] * self._width) + "\n").join(lines) + "\n"

    def __getitem__(self, coord: Coord) -> int:
        return self._board[self._coord_to_index(*coord)]

    def __setitem__(self, coord: Coord, value: int) -> None:
        self._board[self._coord_to_index(*coord)] = value

    def _coord_to_index(self, col: int, row: int) -> int:
        if col < 0 or col >= self._width:
            raise IndexError(f"Bad col {col}")
        if row < 0 or row >= self._height:
            raise IndexError(f"Bad row {row}")

        return row * self._height + col

    def valid_moves(self) -> List[int]:
        valid = []
        for col in range(self._width):
            if self.is_valid_move(col):
                valid.append(col)

        return valid

    def play(self, *, player: int, column: int) -> None:
        if not self.is_valid_move(column):
            raise InvalidMoveError(column)

        for row in reversed(range(self._height)):
            if self[column, row] == 0:
                self[column, row] = player
                break

    def is_valid_move(self, column: int) -> bool:
        return self[column, 0] == 0

    def _check_win_lines(
        self, start_coords: Set[Coord], next_vector: Vector, win_len: int
    ) -> int:
        dc, dr = next_vector
        for c, r in start_coords:
            board_slice = []

            while True:
                # pull out all values into a list; stop on IndexError
                try:
                    value = self[c, r]
                except IndexError:
                    break
                board_slice.append(value)
                r += dr
                c += dc

            for pieces in windowed(board_slice, win_len):
                pieces = set(pieces)
                if 0 not in pieces and None not in pieces and len(pieces) == 1:
                    return pieces.pop()

        return 0

    def check_win(self, win_len: int = 4) -> int:
        for start_coords, vector in self._win_lines:
            result = self._check_win_lines(start_coords, vector, win_len)
            if result != 0:
                return result
        return 0
