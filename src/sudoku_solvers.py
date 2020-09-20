from src.sudoku_objects import Board, CellPointer, Cell

def basic_assign(cell: Cell):
    if sum(cell.candidates) == 1:
        cell.assign_value(cell.candidates.index(1))


def reverse_assign(cell: Cell):
    pass


def basic_eliminate(cell: Cell):
    pass


def group_eliminate(cell: Cell):
    pass


def structure_intersection_eliminate(cell: Cell):
    pass