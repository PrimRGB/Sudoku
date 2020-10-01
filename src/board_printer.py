from src.sudoku_objects import BoardContext
from testing.test_consts import nonempty_board_string
from typing import List
import pandas as pd
import numpy as np
from collections import OrderedDict

def get_board_values(board: BoardContext) -> dict:
    cells = board.cells
    return {pointer.coords: list_to_str_repr(cell.candidates) for pointer, cell in cells.items()}    

def board_values_to_arrays(dict) -> List[list]:
    sorted_vals = OrderedDict(sorted(board_values.items()))
    return [[candidates for coord, candidates in sorted_vals.items() if coord[0]==i] for i in range(9)]

def list_to_str_repr(list) -> str:
    return ''.join([str(i) for i in list])

if __name__=='__main__':
    board_context = BoardContext(nonempty_board_string)
    board_values = get_board_values(board_context)
    board_arrays = board_values_to_arrays(board_values)
    print(pd.DataFrame(board_arrays).to_markdown())
