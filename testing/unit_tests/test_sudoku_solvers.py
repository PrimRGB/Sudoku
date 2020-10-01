import pytest
from src.sudoku_objects import BoardContext
from src.sudoku_solvers import solve_sudoku
from src.board_printer import print_board
from testing.test_consts import nonempty_board_string, easy_board_string


def test_nonempty_board_solver():
    solved_board_state = solve_sudoku(easy_board_string)
    print_board(solved_board_state)
    

if __name__ == '__main__':
    test_nonempty_board_solver()