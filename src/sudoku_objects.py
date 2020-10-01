from typing import Tuple, List, Union
import itertools
from src.metadata import consts


class Board():

    def __init__(self, board_repr: str):
        self.board_repr = board_repr
        self.board_order = int(len(board_repr)**0.25)
        if self.board_order != round(self.board_order):
            raise ValueError("Board size must be a power 4 of an integer.")
        self.board_coords = self.get_board_coords()
        self.board_data = self._parse_board_data()

    def get_board_coords(self):
        return [(x,y) for x,y in itertools.product(range(self.board_order**2),range(self.board_order**2))]

    @staticmethod
    def _get_point_coord(i: int):
        return (i//9, i%9)

    def _parse_board_data(self):
        return dict([(Board._get_point_coord(i), int(self.board_repr[i])) for i in range(len(self.board_repr))])

    def get_empty_cells(self):
        return [coord for coord, value in self.board_data.items() if value == 0]


class CellPointer(Board):
    
    def __init__(self, board: Board, coords: tuple):
        super().__init__(board.board_repr)
        self.coords = coords
        self.triple_coords = CellPointer.get_triple_coords(self.coords)

    @staticmethod
    def get_triple_coords(coords: Tuple[int, int]) -> dict:
        return {'row': coords[0], 'column': coords[1], 'block': (coords[0]//3)*3 + coords[1]//3}

    def partial_peer_coords(self, other_coords: Tuple[int, int], peer_type: str) -> bool:
            return self.triple_coords[peer_type] == CellPointer.get_triple_coords(other_coords)[peer_type]

    def partial_peer(self, other, peer_type: str) -> bool:
        return self.partial_peer_coords(other.coords, peer_type)

    def get_all_partial_peers_coords(self, peer_type) -> List[Tuple[int, int]]:
            return [x for x in self.board_coords if self.partial_peer_coords(x, peer_type)]
   
    def peer_coords(self, other_coords: Tuple[int, int]) -> bool:
        return any([self.partial_peer_coords(other_coords, peer_type) for peer_type in consts.structure_types])
    
    def get_all_peers_coords(self) -> List[Tuple[int, int]]:
        return [coords for coords in self.board_coords if self.peer_coords(coords)]

    def peer(self, other) -> bool:
        return self.peer_coords(other.coords)

    
class Cell(CellPointer):

    def __init__(self, board: Board, pointer: CellPointer):
        super().__init__(board, pointer.coords)
        self.pointer = pointer
        self.value = self.board_data[self.coords]
        self.candidates = [i for i in range(1,10)] if self.value == 0 else [self.value]

    def eliminate_candidates(self, candidates_to_remove: Union[int, List[int]]):
        if len(self.candidates)<2:
            raise ValueError("There must be at least 2 candidates for a cell in order to eliminate a candidate.")
        if type(candidates_to_remove) == int:
            candidates_to_remove = [candidates_to_remove]
        self.candidates = [candidate for candidate in self.candidates if candidate not in candidates_to_remove]

    def assign_value(self, v: int):
        if self.value!=0:
            raise ValueError("A value can only be assigned to an empty cell.")
        if v not in range(1,10):
             raise ValueError("Assigned value can only be between 1 and 9.")
        self.value = v

    # def get_content(self):
    #     if self.value != 0:
    #         return [self.value]
    #     else:
    #         return self.candidates

class BoardContext(Cell):

    def __init__(self, board_repr: str):
        self.board = Board(board_repr)
        self.pointers = {coords: CellPointer(self.board, coords=coords) for coords in self.board.board_coords}
        self.cells = {pointer: Cell(self.board, pointer) for pointer in self.pointers.values()}
    
    def get_structure_cells(self, structure_type: str, structure_index: int) -> List[Cell]:
        structure_pointers = [self.pointers[coords] for coords in self.board.board_coords
                                       if CellPointer.get_triple_coords(coords)[structure_type] == structure_index]
        return [self.cells[pointer] for pointer in structure_pointers]

    def get_board_state(self) -> dict:
        return {pointer.coords: cell.candidates for pointer, cell in self.cells.items()}