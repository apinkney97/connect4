import pytest

from connect4.board import Board, InvalidMoveError


@pytest.mark.parametrize(
    "width, height, col, row, expected",
    [
        (1, 1, 0, 0, 0),
        (20, 20, 0, 0, 0),
        (7, 6, 1, 0, 1),
        (5, 5, 4, 2, 14),
        (100, 100, 99, 99, 9999),
        (10, 10, 1, 1, 11),
    ],
)
def test__coord_to_index(width, height, col, row, expected):
    b = Board(width=width, height=height)
    assert b._coord_to_index(col, row) == expected


def test_play():
    h = 5
    col = 1
    player = 2

    b = Board(width=5, height=h)

    # check board is empty
    for row in range(h):
        assert b[col, row] == 0

    # play until column is full
    for i in range(h):
        b.play(player=player, column=col)

        # check bottom cells are full
        for row_from_bottom in range(i + 1):
            assert b[col, h - row_from_bottom - 1] == player

        # check top cells are empty
        for row in range(h - i - 1):
            assert b[col, row] == 0

    # check can't play again in this column
    with pytest.raises(InvalidMoveError):
        b.play(player=player, column=col)


def test_valid_moves():
    width = 5
    b = Board(width=width, height=1)

    assert set(b.valid_moves()) == set(range(width))

    b.play(player=1, column=0)
    assert set(b.valid_moves()) == set(range(1, width))


@pytest.mark.parametrize(
    "board, win_len, winner",
    [
        ([[0, 0, 0], [0, 0, 0], [2, 1, 2]], 3, 0),  # no winner
        ([[0, 0, 0], [2, 0, 2], [1, 1, 1]], 3, 1),  # 1 wins (bottom row)
        ([[1, 0, 0], [1, 0, 2], [1, 1, 2]], 3, 1),  # 1 wins (first column)
        ([[0, 0, 2], [2, 0, 2], [1, 1, 2]], 3, 2),  # 2 wins (last column)
        (
            [
                [0, 0, 0, 0, 0],
                [0, 2, 0, 2, 0],
                [0, 1, 1, 1, 0],
                [2, 2, 2, 1, 2],
                [2, 1, 1, 1, 1],
            ],
            4,
            1,
        ),  # 1 wins (bottom row)
        (
            [
                [0, 0, 0, 0, 0],
                [0, 2, 0, 2, 0],
                [0, 1, 1, 1, 0],
                [2, 2, 2, 1, 2],
                [2, 1, 1, 1, 1],
            ],
            5,
            0,
        ),  # no winner (need 5 in a row)
        (
            [
                [0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [2, 0, 1, 1, 2],
                [2, 1, 2, 1, 2],
            ],
            3,
            1,
        ),  # vertical
        (
            [
                [0, 0, 0, 0, 0],
                [0, 1, 0, 2, 0],
                [0, 1, 1, 1, 0],
                [2, 2, 2, 1, 2],
                [2, 2, 1, 1, 1],
            ],
            4,
            1,
        ),  # DR diagonal
        (
            [
                [0, 0, 0, 0, 0],
                [0, 1, 0, 2, 0],
                [0, 1, 2, 1, 0],
                [2, 2, 2, 1, 2],
                [2, 2, 1, 1, 1],
            ],
            4,
            2,
        ),  # DL diagonal
    ],
)
def test_check_win(board, win_len, winner):
    b = Board.from_nested_board(board)
    # print(b)
    assert b.check_win(win_len) == winner
