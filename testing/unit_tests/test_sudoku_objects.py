import pytest
from src.sudoku_objects import Board, CellPointer, Cell
from src.metadata import consts
from testing import test_consts


def test_get_empty_cells():
    board = Board(test_consts.empty_board_string)
    assert board.get_empty_cells() == board.board_coords


def test_nonempty_board():
    board = Board(test_consts.nonempty_board_string)
    print(board.board_data)


def test_get_all_peers_coords():
    board = Board(test_consts.nonempty_board_string)
    cp = CellPointer(board, coords=(0,0))
    assert cp.get_all_peers_coords() == test_consts.peers_00


def test_init_cell():
    board = Board(test_consts.nonempty_board_string)
    cp = CellPointer(board, coords=(0,0))
    cell = Cell(board, cp)
    assert cell.value == 4
    assert cell.candidates == []


if __name__=='__main__':
    test_get_empty_cells()
    test_nonempty_board()
    test_get_all_peers_coords()
    test_init_cell()