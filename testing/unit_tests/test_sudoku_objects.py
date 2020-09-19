import pytest
import src.sudoku_objects as sudoku_objects
import testing.test_consts as test_consts
import os


def test_get_empty_cells():
    board = sudoku_objects.Board(test_consts.empty_board_string)
    assert board.get_empty_cells() == board.board_coords


def test_nonempty_board():
    board = sudoku_objects.Board(test_consts.nonempty_board_string)
    print(board.board_data)
    print(os.path.dirname(__file__))


if __name__=='__main__':
    test_get_empty_cells()
    test_nonempty_board()