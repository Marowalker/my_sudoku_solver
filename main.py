import numpy as np

import constants
from solver import *
from generator import *
import pickle

# board = import_problem_from_file('sample.txt')
base = constants.GRID_SIZE
# board = generate_from_base(base)
generate_bulk(num_sample=10, base=base)

with open(constants.BOARD, 'rb') as f:
    boards = pickle.load(f)

all_time = []

for idx, board in enumerate(boards):
    # print(board)
    time_solve, result = solve(board)

    print("Iter: {}. Time taken: {}".format(str(idx + 1), str(time_solve)))
    all_time.append(time_solve)
    # print("Board:")
    # print(get_result(result))

print("Average time:", np.average(all_time))
