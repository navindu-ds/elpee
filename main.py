M = 1000000

import all_stack_start
from alternate_solutions import extract_alternate_solution

is_max = True
n_artificials = 0

# matrix = [[-5, -4, 0, 0, 0], [6, 4, 1, 0, 24], [1, 2, 0, 1, 6]]
# basic_vars = [0, 3, 4]
# n_decision_vars = 2

# matrix = [[-5, -4, 0, 0, 0,  0], 
#           [ 6,  4, 1, 0, 0, 24], 
#           [ 1,  2, 0, 1, 0,  6], 
#           [-1,  1, 0, 0, 1,  1]]
# basic_vars = [0, 3, 4, 5]
# n_decision_vars = 2

# matrix = [[-3, 1, 0, 0, 0], 
#           [4, -1, 1, 0, 8], 
#           [-8, -1, 0, 1, -12]]
# basic_vars = [0, 3, 4]
# n_decision_vars = 2

# matrix = [[-19,-13,-12,-17,  0,  0,  0,  0],
#           [  3,  2,  1,  2,  1,  0,  0,225],
#           [  1,  1,  1,  1,  0,  1,  0,117],
#           [  4,  3,  3,  4,  0,  0,  1,420]]
# basic_vars = [0, 5, 6, 7]
# n_decision_vars = 4

# matrix = [[  1, -2,  1,  0,  0,  0,  0],
#           [  1,  2,  1,  1,  0,  0, 12],
#           [  2,  1, -1,  0,  1,  0,  6],
#           [ -1,  3,  0,  0,  0,  1,  9]]
# basic_vars = [0, 4, 5, 6]
# n_decision_vars = 3
# is_max = False

# matrix = [[ -5, -6,  0,  0,  0],
#           [ -1, -1,  1,  0, -2],
#           [ -4, -2,  0,  1, -4]]
# basic_vars = [0, 3, 4]
# n_decision_vars = 2
# is_max = False

# matrix = [[-3,  1, -1,  0,  0,  0,  0], 
#           [ 4, -1,  0,  1,  0,  0,  8],
#           [-8, -1, -3,  0,  1,  0,-12],
#           [ 5,  0, -1,  0,  0,  1, 13]]
# basic_vars = [0, 4, 5, 6]
# n_decision_vars = 3

# matrix = [[ 1, -2, 0, 0, 0,  0], 
#           [-1, -1, 1, 0, 0, -2], 
#           [ 1, -1, 0, 1, 0, -1], 
#           [ 0,  1, 0, 0, 1,  3]]
# basic_vars = [0, 3, 4, 5]
# n_decision_vars = 2

# matrix = [[-1, -1, 0, 0, 0,  0],
#           [-1,  1, 1, 0, 0,  2],
#           [-6, -4, 0, 1, 0,-24],
#           [ 0, -1, 0, 0, 1, -1]]
# basic_vars = [0, 3, 4, 5]
# n_decision_vars = 2
# is_max = False

# matrix = [[ -2.35, -3, -2.85, 0, 0, 0,    0],
#           [    10,  9,    14, 1, 0, 0, 4000],
#           [     5,  6,    12, 0, 1, 0, 3000],
#           [     0,  1,     0, 0, 0, 1,  250]]
# basic_vars = [0, 4, 5, 6]
# n_decision_vars = 3

# matrix = [[-3, -4, 0, 0, 0, 0,    0],
#           [ 2,  3, 1, 0, 0, 0, 1200],
#           [ 2,  1, 0, 1, 0, 0, 1000],
#           [ 0,  4, 0, 0, 1, 0,  800],
#           [ 1,  4, 0, 0, 0, 1, 1000]]
# basic_vars = [0, 3, 4, 5, 6]
# n_decision_vars = 2

# matrix = [[ 3,  2, 0, 0, 0, 0,  0],
#           [-1, -1, 1, 0, 0, 0, -1],
#           [ 1,  1, 0, 1, 0, 0,  7],
#           [-1, -2, 0, 0, 1, 0,-10],
#           [ 0,  1, 0, 0, 0, 1,  3]]
# basic_vars = [0, 3, 4, 5, 6]
# n_decision_vars = 2

# matrix = [[-24, -6, -1, -2, 0, 0,  0],
#           [ -6, -1,  1,  0, 1, 0, -5],
#           [ -4, -2, -1, -1, 0, 1, -4]]
# basic_vars = [0, 5, 6]
# n_decision_vars = 4
# is_max = False

# matrix = [[ -4, -5, -9, -11, 0, 0, 0,   0],
#           [  1,  1,  1,   1, 1, 0, 0,  15],
#           [  7,  5,  3,   2, 0, 1, 0, 120],
#           [  3,  5, 10,  15, 0, 0, 1, 100]]
# basic_vars = [0, 5, 6, 7]
# n_decision_vars = 4

# matrix = [[ -4, -5, -9, -11, 0, 0, 0, 0,     0],
#           [  1,  1,  1,   1, 1, 0, 0, 0,    15],
#           [  7,  5,  3,   2, 0, 1, 0, 0,   120],
#           [  3,  5, 10,  15, 0, 0, 1, 0,   100],
#           [  3,  4,  7,   5, 0, 0, 0, 1, 500/7]]
# basic_vars = [0, 5, 6, 7, 8]
# n_decision_vars = 4

# matrix = [[0, 0, 1, 0, 0, 15],
#           [1, 1, 1,-1, 0,  5],
#           [1, 0, 0, 1, 0, 10],
#           [0, 0,-1, 1, 1,  5]]
# basic_vars = [0, 2, 1, 5]
# n_decision_vars = 2

# a half solution
# matrix = [[ 0, 13/7, 0, 71/7, -2/7, 0, 10/7, 970/7],
#           [ 1,  5/7, 0, -5/7, 10/7, 0, -1/7,  50/7],
#           [ 0, -6/7, 0, 13/7,-61/7, 1,  4/7, 325/7],
#           [ 0,  2/7, 1, 12/7, -3/7, 0,  1/7,  55/7]]
# basic_vars = [0, 1, 6, 3]
# n_decision_vars = 4

# matrix = [[0, 0, 0, 0, 2, 1, 3, 1827],
#           [1, 1, 0, 0, 1, 2,-1,   39],
#           [0, 1, 1, 0, 0, 4,-1,   48],
#           [0,-1, 0, 1,-1,-5, 2,   30]]
# basic_vars = [0, 1, 3, 4]
# n_decision_vars = 4

# Case with multiple variables to change for alternate solution
matrix = [[0, 0, 0, 0, 2, 1, 1827],
          [1, 1, 0, 2, 1, 2,   39],
          [0, 1, 1, 3, 0, 4,   48]]
basic_vars = [0, 1, 3]
n_decision_vars = 4
new_basic_vars, new_matrix = all_stack_start.solve_linear_programming(basic_vars, matrix, n_decision_vars, is_max, n_artificials)
new_basic_vars, new_matrix = extract_alternate_solution(3, new_basic_vars, new_matrix, is_max, n_decision_vars, n_artificials)

# matrix = [[-1, -1, 0, 0, 0, -M, -M,  0],
#           [-1,  1, 1, 0, 0,  0,  0,  2],
#           [ 6,  4, 0,-1, 0,  1,  0, 24],
#           [ 0,  1, 0, 0,-1,  0,  1,  1]]
# basic_vars = [0, 3, 6, 7]
# n_decision_vars = 2
# n_artificials = 2
# is_max = False

# matrix = [[-6, 7,  4, 0,  0, M, M,  0],
#           [ 2, 5, -1, 1,  0, 0, 0, 18],
#           [-1, 1,  2, 0, -1, 1, 0, 14],
#           [ 3, 2,  2, 0,  0, 0, 1, 26]]
# basic_vars = [0, 4, 6, 7]
# n_decision_vars = 3
# n_artificials = 2
# is_max = True

# matrix = [[-3,  1, -1, 0,  0, 0, M,  0],
#           [ 4, -1,  0, 1,  0, 0, 0,  8],
#           [ 8,  1,  3, 0, -1, 0, 1, 12],
#           [ 5,  0, -1, 0,  0, 1, 0, 13]]
# basic_vars = [0, 4, 7, 6]
# n_decision_vars = 3
# n_artificials = 1
# is_max = True

# # Test for this
# matrix = [[  1, -2,  0,  0,  0,  M,  M, 0],
#           [  1,  1, -1,  0,  0,  1,  0, 2],
#           [ -1,  1,  0, -1,  0,  0,  1, 1],
#           [  0,  1,  0,  0,  1,  0,  0, 3]]
# basic_vars = [0, 6, 7, 5]
# n_decision_vars = 2
# n_artificials = 2
# is_max = True

# matrix = [[-6,  4,  0,  0, -M, -M, 0],
#           [ 3,  1,  1,  0,  0,  0, 5],
#           [-6,  4,  0, -1,  1,  0, 2],
#           [ 2,  5,  0,  0,  0,  1, 6]]
# basic_vars = [0, 3, 5, 6]
# n_decision_vars = 2
# n_artificials = 2
# is_max = False

# matrix = [[-6,  4,  0,  0, -M,  0],
#           [ 3,  1,  1,  0,  0,  5],
#           [ 6, -4,  0,  1,  0, -2],
#           [ 2,  5,  0,  0,  1,  6]]
# basic_vars = [0, 3, 4, 5]
# n_decision_vars = 2
# n_artificials = 1
# is_max = False

# matrix = [[-0.50, -0.5,  0,  0,  0,   0],
#           [ 0.30,  0.1,  1,  0,  0, 2.7],
#           [ 0.50,  0.5,  0,  1,  0, 6.0],
#           [ 0.60,  0.4,  0,  0,  1, 6.0]]
# basic_vars = [0, 3, 4, 5]
# n_decision_vars = 2
# n_artificials = 0
# is_max = True

# matrix = [[0, -1/3, 0, -1/6, 0, 13/3],
#           [0,  5/3, 1, -1/6, 0, 13/3],
#           [1,  2/3, 0, -1/6, 0, 10/3],
#           [0,   -1, 0,    0, 1,    2]]
# basic_vars = [0, 3, 1, 5]
# n_decision_vars = 2
# n_artificials = 1
# is_max = False

# all_stack_start.solve_linear_programming(basic_vars, matrix, n_decision_vars, is_max, n_artificials)