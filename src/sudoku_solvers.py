from src.sudoku_objects import Board, CellPointer, Cell, BoardContext
from src.metadata import consts
from itertools import combinations

class SudokuSolver(BoardContext):

    def __init__(self, board_repr: str):
        super().__init__()

    @staticmethod
    def basic_assign(cell: Cell):
        if len(cell.candidates) == 1:
            cell.assign_value(cell.candidates[0])
    
    def reverse_assign(self, pointer: CellPointer):
        for peer_type in consts.structure_types:
            partial_peers_candidates = [self.cells[peer].candidates 
                                for peer in pointer.get_all_partial_peers_coords(type=peer_type)]
            structure_candidates = set(range(1,10)) - set().union(*partial_peers_candidates)
            if len(structure_candidates) == 1:
                self.cells[pointer].assign_value(list(structure_candidates)[0])
            
    def basic_eliminate(self, cell: Cell):
        if cell.value !=0:
            peer_cells = [self.cells[peer] for peer in cell.get_all_peers_coords]
            for peer_cell in peer_cells:
                peer_cell.candidates.remove(cell.value)

    def group_eliminate(self, structure_type: str, structure_index: int):
        structure_cells = self.get_structure_cells(structure_type, structure_index)
        for subset_size in reversed(range(1,9)):
            relevant_cells = [cell for cell in structure_cells if len(cell.candidates)>=subset_size]
            for subset in combinations(relevant_cells, subset_size):
                subset_candidates = [cell.candidates for cell in subset]
                common_subset_candidates = sorted(list(set.intersection(*subset_candidates)))
                if len(common_subset_candidates) == subset_size:
                    structure_subset_complement = [cell for cell in structure_cells if cell not in subset_candidates]
                    for cell in structure_subset_complement:
                        cell.candidates.remove(common_subset_candidates)
                    for cell in subset:
                        cell.candidates = common_subset_candidates

    def structure_intersection_eliminate(self, row_or_column: str, row_or_column_index: int, block_index: int):
        row_or_column_cells = self.get_structure_cells(row_or_column, row_or_column_index)
        block_cells = self.get_structure_cells('block', block_index)
        row_or_column_only_candidates = [cell.candidates for cell in row_or_column_cells
                                        if cell not in block_cells]
        total_row_or_column_candidates = set.union(*row_or_column_only_candidates)
        block_only_cells = [cell for cell in block_cells 
                            if cell not in row_or_column_cells]
        if len(total_row_or_column_candidates) < 9:
            complement_digits = [digit for digit in list(range(1,10)) 
            if digit not in total_row_or_column_candidates] 
            for cell in block_only_cells:
                cell.remove(complement_digits)
