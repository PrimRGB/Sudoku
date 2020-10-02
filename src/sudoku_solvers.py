from itertools import combinations
from copy import deepcopy
from src.sudoku_objects import Board, CellPointer, Cell, BoardContext
from src.metadata.consts import structure_types
from src.board_printer import print_board

class SudokuSolver(BoardContext):

    def __init__(self, board_repr: str):
        super().__init__(board_repr)


    def basic_assign(self, cell: Cell):
        if len(cell.candidates) == 1 and cell.value == 0:
            cell.assign_value(cell.candidates[0])
    
    def reverse_assign(self, cell: Cell):
        if cell.value == 0:
            for peer_type in structure_types:
                partial_peer_pointers = [self.pointers[peer_coords] 
                                        for peer_coords in cell.get_all_partial_peers_coords(peer_type=peer_type)]
                partial_peers_candidates = [self.cells[peer].candidates 
                                            for peer in partial_peer_pointers]
                structure_candidates = set(range(1,10)) - set().union(*partial_peers_candidates)
                if len(structure_candidates) == 1:
                    cell.assign_value(list(structure_candidates)[0])
                    break
            
    def basic_eliminate(self, cell: Cell):
        if cell.value != 0:
            peer_pointers = [self.pointers[peer_coords] for peer_coords in cell.get_all_peers_coords()]
            peer_cells = [self.cells[peer_pointer] for peer_pointer in peer_pointers]
            for peer_cell in peer_cells:
                if cell.value in peer_cell.candidates:
                    peer_cell.eliminate_candidates(cell.value)

    def group_eliminate(self, structure_type: str, structure_index: int):
        structure_cells = self.get_structure_cells(structure_type, structure_index)
        for subset_size in reversed(range(1,9)):
            relevant_cells = [cell for cell in structure_cells if len(cell.candidates)==subset_size]
            for subset in combinations(relevant_cells, subset_size):
                subset_candidates = [set(cell.candidates) for cell in subset]
                common_subset_candidates = sorted(list(set.intersection(*subset_candidates)))
                if len(common_subset_candidates) == subset_size:
                    complement_subset = [cell for cell in structure_cells if cell not in subset]
                    for cell in complement_subset:
                        cell.eliminate_candidates(common_subset_candidates)
                    for cell in subset:
                        cell.candidates = common_subset_candidates
                    return

    def structure_intersection_eliminate(self, row_or_column: str, row_or_column_index: int, block_index: int):
        row_or_column_cells = self.get_structure_cells(row_or_column, row_or_column_index)
        block_cells = self.get_structure_cells('block', block_index)
        row_or_column_only_cells = [cell for cell in row_or_column_cells if cell not in block_cells]
        block_only_cells = [cell for cell in block_cells if cell not in row_or_column_cells]
        block_only_candidates = [set(cell.candidates) for cell in block_only_cells]
        total_block_candidates = sorted(list(set.union(*block_only_candidates)))
        if len(total_block_candidates) < 9:
            complement_candidates = [candidate for candidate in list(range(1,10)) if candidate not in total_block_candidates]
            for cell in row_or_column_only_cells:
                cell.eliminate_candidates(complement_candidates)


def solve_sudoku(board_repr: str):
    solver = SudokuSolver(board_repr)
    steps_count = 0
    progress = 1
    
    while progress==1:
        board_state = deepcopy(solver.get_board_state())
    
        for cell in solver.cells.values():
            solver.basic_assign(cell)
    
        for cell in solver.cells.values():
            solver.basic_eliminate(cell)
    
        for cell in solver.cells.values():
            solver.reverse_assign(cell)
    
        for structure_type, structure_index in zip(structure_types, range(9)):
            solver.group_eliminate(structure_type, structure_index)
    
        for row_or_column, row_or_column_index, block_index in zip(structure_types[:2], range(9), range(9)):
            solver.structure_intersection_eliminate(row_or_column, row_or_column_index, block_index)
        
        if solver.get_board_state() == board_state and steps_count>1:
            progress = 0
        steps_count+=1

    print('Total steps:', steps_count)
    return solver.get_board_state()
