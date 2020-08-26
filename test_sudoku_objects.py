import pytest
import sudoku_objects


def test_empty_board():
    empty_board = sudoku_objects.Board('0'*81)
    assert empty_board.get_empty_cells() == [(0,0)]*81


if __name__=='__main__':
    test_empty_board()