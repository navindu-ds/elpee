import all_stack_start

is_max = True

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

# # failed case - infinite loop
# matrix = [[-3,  1, -1,  0,  0,  0,  0], 
#           [ 4, -1,  0,  1,  0,  0,  8],
#           [-8, -1, -3,  0,  1,  0,-12],
#           [ 5,  0, -1,  0,  0,  1, 13]]
# basic_vars = [0, 4, 5, 6]
# n_decision_vars = 3

# # failed case - infinite loop
# matrix = [[ 1, -2, 0, 0, 0, 0], 
#           [-1, -1, 1, 0, 0, -2], 
#           [ 1, -1, 0, 1, 0, -1], 
#           [ 5,  0, 0, 0, 1, 3]]
# basic_vars = [0, 3, 4, 5]
# n_decision_vars = 2

matrix = [[-1, -1, 0, 0, 0,  0],
          [-1,  1, 1, 0, 0,  2],
          [-6, -4, 0, 1, 0,-24],
          [ 0, -1, 0, 0, 1, -1]]
basic_vars = [0, 3, 4, 5]
n_decision_vars = 2
is_max = False

# print(next_simplex_sol(basic_vars, matrix, True))
all_stack_start.solve_linear_programming(basic_vars, matrix, n_decision_vars, is_max)