import pytest
from copy import deepcopy
from src.sudoku_objects import Board, CellPointer, Cell, BoardContext
from src.board_printer import print_board
from src.metadata import consts
from testing import test_consts

def test_get_empty_cells():
    board = Board(test_consts.empty_board_string)
    assert board.get_empty_cells() == board.board_coords


def test_nonempty_board():
    board = Board(test_consts.nonempty_board_string)
    assert board.board_data == test_consts.nonempty_board_data

def test_get_all_peers_coords():
    board = Board(test_consts.nonempty_board_string)
    pointer = CellPointer(board, coords=(0,0))
    assert pointer.get_all_peers_coords() == test_consts.peers_00

def test_init_cell():
    board = Board(test_consts.nonempty_board_string)
    pointer = CellPointer(board, coords=(0,0))
    cell = Cell(board, pointer)
    assert cell.value == 4
    assert cell.candidates == [4]

def test_assign_value():
    board = Board(test_consts.nonempty_board_string)
    pointer = CellPointer(board, coords=(0,1))
    cell = Cell(board, pointer)
    cell.assign_value(5)
    assert cell.value == 5

def test_eliminate_candidates():
    board = Board(test_consts.nonempty_board_string)
    pointer = CellPointer(board, coords=(0,1))
    cell = Cell(board, pointer)
    old_candidates = deepcopy(cell.candidates)
    cell.eliminate_candidates(5)
    assert cell.candidates == [candidate for candidate in old_candidates if candidate!=5]

def changed_board_state():
    board_context = BoardContext(test_consts.nonempty_board_string)
    initial_board_state = deepcopy(board_context.get_board_state())
    board_context.cells[board_context.pointers[(0,1)]].candidates = [5]
    assert initial_board_state != board_context.get_board_state()


if __name__=='__main__':
    test_get_empty_cells()
    test_nonempty_board()
    test_get_all_peers_coords()
    test_init_cell()
    test_assign_value()
    test_eliminate_candidates()
    changed_board_state()
    