from src.sudoku_objects import BoardContext
from testing.test_consts import nonempty_board_string
from typing import List, Optional
import pandas as pd
from collections import OrderedDict

def prettify_candidates(candidates: list) -> str:
    return ''.join([str(candidate) for candidate in candidates])

def get_pretty_board_state(board_context: BoardContext) -> dict:
    board_state = board_context.get_board_state()
    return {coords: prettify_candidates(candidates) for coords,candidates in board_state.items()}

def get_board_arrays(board_context: BoardContext, output_type: str='candidates') -> List[list]:
    if output_type == 'candidates':
        pretty_board = get_pretty_board_state(board_context)
    if output_type == 'values':
        pretty_board = board_context.get_board_values()
    sorted_vals = OrderedDict(sorted(pretty_board.items()))
    return [[cell_content for coord, cell_content in sorted_vals.items() if coord[0]==i] for i in range(int(len(pretty_board)**0.5))]

def print_board(board_context: BoardContext, output_type: str='candidates'):
    board_arrays = get_board_arrays(board_context, output_type)
    print(pd.DataFrame(board_arrays).to_markdown(tablefmt="grid"))

if __name__=='__main__':
    board_context = BoardContext(nonempty_board_string)
    print_board(board_context=board_context)
    