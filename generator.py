from random import sample
import pickle


def generate_from_base(base):
    side = base * base

    # pattern for a baseline valid solution
    def pattern(r, c): return (base * (r % base) + r // base + c) % side

    # randomize rows, columns and numbers (of valid base pattern)
    def shuffle(s): return sample(s, len(s))

    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base * base + 1))

    # produce board using randomized baseline pattern
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    # remove numbers to make a sudoku problem
    squares = side * side
    empties = squares * 3 // 4
    for p in sample(range(squares), empties):
        board[p // side][p % side] = 0

    return board


def generate_bulk(num_sample, base):
    all_boards = []
    for i in range(num_sample):
        board = generate_from_base(base)
        all_boards.append(board)
    size = str(base * base) + 'x' + str(base * base)
    with open('puzzles_' + size + '.pkl', 'wb') as f:
        pickle.dump(all_boards, f)
