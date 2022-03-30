import numpy as np

import constants
from solver import *
from generator import *
import pickle
from sudoku import Sudoku

# board = import_problem_from_file('sample.txt')
base = constants.GRID_SIZE
# board = generate_from_base(base)
# generate_bulk(num_sample=10, base=base)

with open(constants.BOARD, 'rb') as f:
    boards = pickle.load(f)

all_time = []

# board = boards[0]
#
# sudoku_board = Sudoku(3, 3, board=board)
# sudoku_board.show()

# time_solve, result = solve(board)

# print("Time taken: {}".format(str(time_solve)))
# all_time.append(time_solve)
# print("Board:")
# solved = get_result(result)
# print(solved)
# sudoku_board = Sudoku(3, board=solved.tolist())
# sudoku_board.show()

for idx, board in enumerate(boards):
    # print(board)
    time_solve, result = solve(board)

    print("Iter: {}. Time taken: {}".format(str(idx + 1), str(time_solve)))
    all_time.append(time_solve)
    print("Board:")
    print(get_result(result))
#
# print("Average time:", np.average(all_time))
