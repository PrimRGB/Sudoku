from src.sudoku_objects import Board, CellPointer, Cell

class SudokuSolver(Cell):
    def __init__(self, board_coords):
        self.board = Board(board_coords)
        self.pointers = {coords: CellPointer(self.board, coords = coords) for coords in board_coords}
        self.cells = {pointer: Cell(self.board, pointer) for pointer in self.pointers}

    @staticmethod
    def basic_assign(cell: Cell):
        if sum(cell.candidates) == 1:
            cell.assign_value(cell.candidates.index(1))


    def reverse_assign(self, pointer: CellPointer):
        row_peers_candidates = [self.cells[peer].candidates 
                                for peer in pointer.get_all_row_peers_coords()]
        column_peers_candidates = [self.cells[peer].candidates 
                                for peer in pointer.get_all_column_peers_coords()]
        block_peers_candidates = [self.cells[peer].candidates 
                                  for peer in pointer.get_all_block_peers_coords()]
        
        row_candidates = set(range(1,10)) - set().union(*row_peers_candidates)
        column_candidates = set(range(1,10)) - set().union(*column_peers_candidates)
        block_candidates = set(range(1,10)) - set().union(*block_peers_candidates)
        
        if len(row_candidates) == 1:
            self.cells[pointer].assign_value(list(row_candidates)[0])
        elif len(column_candidates) == 1:
            self.cells[pointer].assign_value(list(column_candidates)[0])
        elif len(block_candidates) == 1:
            self.cells[pointer].assign_value(list(block_candidates)[0])

    def basic_eliminate(cell: Cell):
        pass


    def group_eliminate(cell: Cell):
        pass


    def structure_intersection_eliminate(cell: Cell):
        pass