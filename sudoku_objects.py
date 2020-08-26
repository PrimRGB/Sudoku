import numpy as np
import consts
import sudoku_exceptions
# from typing import List


class Board():
    def __init__(self, board_repr, board_coords=consts.board_coords):
        self.board_repr = board_repr
        self.board_square = len(board_repr)**0.5
        if self.board_square != round(self.board_square):
            raise ValueError("Board must be square sized.")
        self.board_coords = board_coords
        self.board_data = self._parse_board_data()

    def _parse_board_data(self):
        return dict(
                    zip([(int(self.board_repr[i//9]), int(self.board_repr[i%9])) for i in range(len(self.board_repr))], 
                        [int(i) for i in range(len(self.board_repr))])
                    )

    def get_empty_cells(self):
        return [coord for coord, value in self.board_data.items() if value == 0]

# class CellPointers(Board):

#     def __init__(self, coords: tuple):
#         self.coords = coords
#         super().__init__()

#     def get_row(self) -> int:
#         return self.coords[0]

#     def get_column(self) -> int:
#         return self.coords[1]
    
#     def get_block(self) -> int:
#         return 3*self.coords[0] + self.coords[1]
    
#     def is_same_row(self, other) -> bool:
#         return self.get_row() == other.get_row()

#     def is_same_column(self, other) -> bool:
#         return self.get_column() == other.get_column()

#     def is_same_block(self, other) -> bool:
#         return self.get_block() == other.get_block()

#     def is_peer(self, other) -> bool:
#         return (self.is_same_row(other) or self.is_same_column(other) or self.is_same_block(other))

#     def get_all_peers(self) -> List[tuple]:
#         return [x for x in self.board_coords if self.is_peer(x)]

    
# class Cell(CellPointers):
#     def __init__(self, cell_pointer: CellPointer):
#         #super().__init__()
#         self.coords = cell_pointer.coords
#         self.candidates = [1 for i in range(9)]
#         self.value = self.board_data[self.coords]

#     def eliminate_candidate(self, d):
#         if sum(self.candidates)>=2:
#             raise sudoku_exceptions.NotEnoughCandidatesException("There must be at least 2 candidates for a cell in order to eliminate a candidate.")
#         self.candidates[d+1]=0

#     def assign_value(self, v: int):
#         if self.value!=0:
#             raise sudoku_exceptions.CellAssignmentException("A value can only be assigned to an empty cell.")
#         if v not in range(1,10):
#              raise sudoku_exceptions.CellAssignmentException("Assigned value can only be between 1 and 9.")
#         self.value = v

# def basic_assign(cell: Cell):
#     if sum(cell.candidates) == 1:
#         cell.assign_value(cell.candidates.index(1))


# class Structure(Cell):
#     def __init__(self, structure_type: str, structure_index: int):
#         pass

