def basic_assign(cell: Cell):
    if sum(cell.candidates) == 1:
        cell.assign_value(cell.candidates.index(1))
