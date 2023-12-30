import all_stack_start

# matrix = [[-5, -4, 0, 0, 0], [6, 4, 1, 0, 24], [1, 2, 0, 1, 6]]
# basic_vars = [0, 3, 4]

# matrix = [[-5, -4, 0, 0, 0, 0], [6, 4, 1, 0, 0, 24], [1, 2, 0, 1, 0, 6], [-1, 1, 0, 0, 1, 1]]
# basic_vars = [0, 3, 4, 5]

# matrix = [[-3, 1, 0, 0, 0], [4, -1, 1, 0, 8], [-8, -1, 0, 1, -12]]
# basic_vars = [0, 3, 4]

# # failed case
# matrix = [[1, -2, 0, 0, 0, 0], [-1, -1, 1, 0, 0, -2], [1, -1, 0, 1, 0, -1], [5, 0, 0, 0, 1, 3]]
# basic_vars = [0, 3, 4, 5]

matrix = [[-3, 1, -1, 0, 0, 0, 0], [4, -1, 0, 1, 0, 0, 8], [-8, -1, -3, 0, 1, 0, -12], [5, 0, -1, 0, 0, 1, 13]]
basic_vars = [0, 4, 5, 6]

# print(next_simplex_sol(basic_vars, matrix, True))
all_stack_start.solve_linear_programming(basic_vars, matrix, True)