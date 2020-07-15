import numpy as np
import consts
import soduko_exceptions
from typing import List

class Cell():
    def __init__(self, coords: tuple):
        self.coords = coords
        self.candidates = [1 for i in range(9)]
        self.value = 0
    
    def __repr__(self):
        return f'{self.coords}: {self.value}, [{self.candidates}]'

    def get_row(self) -> int:
        return self.coords[0]

    def get_column(self) -> int:
        return self.coords[1]
    
    def get_block(self) -> int:
        return 3*self.coords[0] + self.coords[1]
    
    def is_same_row(self, other) -> bool:
        return self.get_row() == other.get_row()

    def is_same_column(self, other) -> bool:
        return self.get_column() == other.get_column()

    def is_same_block(self, other) -> bool:
        return self.get_block() == other.get_block()

    def is_peer(self, other) -> bool:
        return (self.is_same_row(other) or self.is_same_column(other) or self.is_same_block(other))
    
    def eliminate_candidate(self, d):
        if sum(self.candidates)>=2:
            raise soduko_exceptions.NotEnoughCandidatesException("There must be at least 2 candidates for a cell in order to eliminate a candidate.")
        self.candidates[d+1]=0

    def assign_value(self, v: int):
        if self.value!=0:
            raise soduko_exceptions.CellAssignmentException("A value can only be assigned to an empty cell.")
        if v not in range(1,10):
             raise soduko_exceptions.CellAssignmentException("Assigned value can only be between 1 and 9.")
        self.value = v


def basic_assign(cell: Cell):
    if sum(cell.candidates) == 1:
        cell.assign_value(cell.candidates.index(1))
