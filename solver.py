from pysat.solvers import Glucose3, Minisat22
import numpy as np
import time
import constants
import math


N = constants.BOARD_SIZE  # Size of the full board
grid = constants.GRID_SIZE  # Size of each small section of the board, = sqrt(N)
num_var = N * N * N


# utility function to check for the use of the subgrid rule
def is_square(i: int) -> bool:
    return i == math.sqrt(i) ** 2


def import_problem_from_file(filename):
    res = np.zeros([N, N], dtype=int)

    with open(filename) as f:
        lines = f.readlines()

    for line in lines:
        values = line.split()
        r, c, v = [int(i) for i in values]
        res[r - 1][c - 1] = v

    return res.tolist()


# encoding the index of each cell
def cell(row, col, value):
    return N * N * (row - 1) + N * (col - 1) + value


# turn the encoded value back to cell values (row, column, digit)
def decode_cell(var):
    r = int((var - 1) / (N * N))
    c = int((var - r * N * N - 1) / N)
    v = var - r * N * N - c * N
    return r + 1, c + 1, v


# binomial (simple) encoding for the digit rule
def encode_digit():
    cls = []
    # for all cells, ensure that the each cell:
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            # denotes (at least) one of the (N - 1) digits (1 clause)
            cls.append([cell(i, j, d) for d in range(1, N + 1)])
            # does not denote two different digits at once (36 clauses)
            for d in range(1, N + 1):
                for dp in range(d + 1, N + 1):
                    cls.append([-cell(i, j, d), -cell(i, j, dp)])
    return cls


# sub function to be used in all rows/columns/subgrids rules
def encode_region(cells):
    cls = []
    # for each pair of cells in a specified region
    for i in range(len(cells) - 1):
        for j in range(i + 1, len(cells)):
            x_i = cells[i]
            x_j = cells[j]
            # each pair does not denote the same digit; a.k.a only one digit can be present in a specified region
            for d in range(1, N + 1):
                cls.append([-cell(x_i[0], x_i[1], d), -cell(x_j[0], x_j[1], d)])
    return cls


# sequential counter encoding for the digit rule
def encode_sequence():
    cls = []
    new_var = []
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            # denotes (at least) one of the (N - 1) digits (1 clause)
            cls.append([cell(i, j, d) for d in range(1, N + 1)])
            # create variables s_i
            for d in range(1, N + 1):
                new_var.append(cell(i, j, d) + num_var)

    # since there is only N - 1 s_i variables, we drop the last element
    new_var = new_var[:-1]
    # sequential counter encoding for N regular variables and N-1 s_i variables
    for idx, var in enumerate(new_var):
        # get the cell function
        r, c, v = decode_cell(var - num_var)
        if idx + 1 == 1:
            cls.append([-cell(r, c, v), var])
        elif idx + 1 == num_var - 1:
            r, c, v = decode_cell(var - num_var + 1)
            cls.append([-var, -cell(r, c, v)])
        else:
            cls.append([-cell(r, c, v), var])
            cls.append([-new_var[idx - 1], var])
            cls.append([-new_var[idx - 1], -cell(r, c, v)])

    return cls


def encode_row():
    cls = []
    for i in range(1, N + 1):
        temp_cls = encode_region([(i, j) for j in range(1, N + 1)])
        cls += temp_cls
    return cls


def encode_col():
    cls = []
    for j in range(1, N + 1):
        temp_cls = encode_region([(i, j) for i in range(1, N + 1)])
        cls += temp_cls
    return cls


def encode_subgrid():
    cls = []
    # for each grid
    for i in range(1, N + 1, grid):
        for j in range(1, N + 1, grid):
            temp_cls = encode_region([(i + d % grid, j + d // grid) for d in range(N)])
            cls += temp_cls
    return cls


def encode_clauses(board):
    # if subgrids exist in the board
    if is_square(len(board)):
        # all_clauses = encode_digit() + encode_row() + encode_col() + encode_subgrid()
        all_clauses = encode_sequence() + encode_row() + encode_col() + encode_subgrid()
    else:
        all_clauses = encode_sequence() + encode_row() + encode_col()
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            d = board[i - 1][j - 1]
            if d:
                all_clauses.append([cell(i, j, d)])
    # unique_clauses = set(tuple(i) for i in all_clauses)
    # return [list(i) for i in unique_clauses]
    return all_clauses


def solve(board):
    clauses = encode_clauses(board)
    # Print number SAT clause
    numclause = len(clauses)
    print("P CNF " + str(numclause) + " (number of clauses)")
    # solve the SAT problem
    # sol = Glucose3()
    sol = Minisat22()
    for c in clauses:
        sol.add_clause(c)
    start = time.process_time()
    sol.solve()
    end = time.process_time()
    t = end - start
    # print("Time: " + str(t))
    result = sol.get_model()

    return t, result


def get_result(result):

    def decode(input_result):
        res = []
        for i in range(1, num_var + 1):
            if input_result[i - 1] > 0:
                r, c, v = decode_cell(input_result[i - 1])
                res.append([r, c, v])
        return res

    result = decode(result)

    result_sudoku = np.zeros([N, N], dtype=int)

    for data in result:
        r = int(data[0])
        c = int(data[1])
        val = data[2]
        result_sudoku[r - 1][c - 1] = val

    return result_sudoku


# test_cells = [(1, 1), (2, 2), (3, 3)]
# print(encode_sequence(test_cells))

encode_sequence()
