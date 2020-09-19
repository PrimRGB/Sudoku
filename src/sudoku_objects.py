import numpy as np
import src.metadata.consts as consts
from src import sudoku_exceptions
from typing import Tuple, List


class Board():
    def __init__(self, board_repr: str, board_coords: List[tuple]=consts.board_coords):
        self.board_repr = board_repr
        self.board_square = len(board_repr)**0.5
        if self.board_square != round(self.board_square):
            raise ValueError("Board must be square sized.")
        self.board_coords = board_coords
        self.board_data = self._parse_board_data()


    @staticmethod
    def _get_point_coord(i: int):
        return (i//9, i%9)


    def _parse_board_data(self):
        return dict([(Board._get_point_coord(i), int(self.board_repr[i])) for i in range(len(self.board_repr))])


    def get_empty_cells(self):
        return [coord for coord, value in self.board_data.items() if value == 0]


class CellPointer(Board):
    def __init__(self, board: Board, coords: tuple):
        super().__init__(board.board_repr, board.board_coords)
        self.coords = coords
        self.row = CellPointer.get_row(self.coords)
        self.column = CellPointer.get_column(self.coords)
        self.block = CellPointer.get_block(self.coords)

    @staticmethod
    def get_row(coord: Tuple[int,int]) -> int:
        return coord[0]


    @staticmethod
    def get_column(coord: Tuple[int, int]) -> int:
        return coord[1]


    @staticmethod
    def get_block(coord: Tuple[int, int]) -> int:
        return coord[0]//3+coord[1]//3


    def peer_coords(self, other_coords: Tuple[int, int]) -> bool:
        return (self.row == CellPointer.get_row(other_coords)) or \
        (self.column == CellPointer.get_column(other_coords)) or \
        (self.block == CellPointer.get_block(other_coords))


    def peer(self, other) -> bool:
        return (self.row == other.row) or (self.column == other.column) or (self.block == other.block)
    

    def get_peers_coords(self) -> List[tuple]:
        return [x for x in self.board_coords if self.peer_coords(x)]
    

    
class Cell(CellPointer):
    def __init__(self, board: Board, pointer: CellPointer):
        super().__init__(board.board_repr, board.board_coords, pointer.coords)
        self.candidates = [i for i in range(1,10)]
        self.value = self.board_data[self.coords]


    def eliminate_candidate(self, c: int):
        if len(self.candidates)<2:
            raise sudoku_exceptions.NotEnoughCandidatesException("There must be at least 2 candidates for a cell in order to eliminate a candidate.")
        self.candidates.remove(c)


    def assign_value(self, v: int):
        if self.value!=0:
            raise sudoku_exceptions.CellAssignmentException("A value can only be assigned to an empty cell.")
        if v not in range(1,10):
             raise sudoku_exceptions.CellAssignmentException("Assigned value can only be between 1 and 9.")
        self.value = v

