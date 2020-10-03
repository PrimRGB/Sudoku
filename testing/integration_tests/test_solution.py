import pytest
from src.sudoku_objects import BoardContext
from src.sudoku_solvers import solve_sudoku
from src.board_printer import print_board
from testing.test_consts import nonempty_board_string, easy_board_string
from src.evaluation import evaluate_board_validity


def test_nonempty_board_solver():
    board_string = easy_board_string
    board = BoardContext(board_string)
    print_board(board, output_type='values')
    print('SOLUTION:')
    solved_board = solve_sudoku(board_string)
    print_board(solved_board)
    evaluate_board_validity(solved_board)    

if __name__ == '__main__':
    test_nonempty_board_solver()
