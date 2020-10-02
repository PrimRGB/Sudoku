import pytest
from copy import deepcopy
from src.sudoku_objects import BoardContext
from src.sudoku_solvers import SudokuSolver
from src.board_printer import print_board
from testing.test_consts import nonempty_board_string, easy_board_string

def test_basic_eliminate():
    solver = SudokuSolver(nonempty_board_string)
    test_cell = solver.cells[solver.pointers[(0,0)]]
    peer_cell = solver.cells[solver.pointers[(0,1)]]
    peer_cell_old_candidates = deepcopy(peer_cell.candidates)
    solver.basic_eliminate(test_cell)
    assert peer_cell.candidates == [candidate for candidate in peer_cell_old_candidates if candidate != test_cell.value]

def test_reverse_assign():
    solver = SudokuSolver(nonempty_board_string)
    first_row = solver.get_structure_cells('row', 0)
    test_cell = solver.cells[solver.pointers[(0,1)]]
    first_row.remove(test_cell)
    for cell in first_row:
        if cell.value == 0:
            cell.eliminate_candidates(1)    
    solver.reverse_assign(test_cell)
    assert test_cell.value == 1

def test_group_eliminate():
    solver = SudokuSolver(nonempty_board_string)
    test_cell = solver.cells[solver.pointers[(0,1)]]
    test_cell_old_candidates = deepcopy(test_cell.candidates)
    solver.cells[solver.pointers[(2,1)]].eliminate_candidates([1,2,3,4,5,6,7])
    solver.cells[solver.pointers[(2,2)]].eliminate_candidates([1,2,3,4,5,6,7])
    solver.group_eliminate('block', 0)
    assert test_cell.candidates == [candidate for candidate in test_cell_old_candidates if candidate not in [8,9]]

def test_structure_intersection_eliminate():  
    solver = SudokuSolver(nonempty_board_string)
    test_cell = solver.cells[solver.pointers[(1,4)]]
    test_cell_old_candidates = deepcopy(test_cell.candidates)
    print(test_cell_old_candidates)
    cells_to_alter = [cell for cell in solver.get_structure_cells('block', 0)
                      if (cell in solver.get_structure_cells('row', 0) 
                      or cell in solver.get_structure_cells('row', 2))]
    for cell in cells_to_alter:
        cell.eliminate_candidates(9)
    solver.structure_intersection_eliminate('row', 1 ,0)
    print_board(solver.get_board_state())
    assert test_cell.candidates == [candidate for candidate in test_cell_old_candidates if candidate!=9]


if __name__ == '__main__':
    test_basic_eliminate()
    test_reverse_assign()
    test_group_eliminate()
    test_structure_intersection_eliminate()