import numpy as np

import constants
from solver import *
from generator import *
import pickle
from sudoku import Sudoku

base = constants.GRID_SIZE
# generate_bulk(num_sample=10, base=base)

with open(constants.BOARD, 'rb') as f:
    boards = pickle.load(f)

all_time = []

for idx, board in enumerate(boards):
    # print(board)
    time_solve, result = solve(board, mode='sequential')

    print("Iter: {}. Time taken: {}".format(str(idx + 1), str(time_solve)))
    all_time.append(time_solve)
    print("Board:")
    solved = get_result(result)
    sudoku_board = Sudoku(base, board=solved.tolist())
    sudoku_board.show()

print("Average time:", np.average(all_time))
