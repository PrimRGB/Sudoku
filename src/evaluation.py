from src.sudoku_objects import Cell, BoardContext
from src.metadata.consts import structure_types

def evaluate_value_validity(board_context: BoardContext):
    for cell in board_context.cells.values():
        peer_pointers = [board_context.pointers[peer_coords] for peer_coords in cell.get_all_peers_coords()]
        peer_cells = [board_context.cells[peer_pointer] for peer_pointer in peer_pointers]
        for peer_cell in peer_cells:
            assert cell.value != peer_cell.value
                
def evaluate_candidate_validity(board_context: BoardContext):
    for cell in board_context.cells.values():
        peer_pointers = [board_context.pointers[peer_coords] for peer_coords in cell.get_all_peers_coords()]
        peer_cells = [board_context.cells[peer_pointer] for peer_pointer in peer_pointers]
        for peer_cell in peer_cells:
            assert peer_cell.value not in cell.candidates

def evaluate_board_validity(board_context: BoardContext):
    evaluate_value_validity(board_context)
    evaluate_candidate_validity(board_context)
    print('Board is valid.')