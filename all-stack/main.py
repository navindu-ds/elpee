import all_stack_start

# matrix = [[-5, -4, 0, 0, 0], [6, 4, 1, 0, 24], [1, 2, 0, 1, 6]]
# basic_vars = [0, 3, 4]

matrix = [[-5, -4, 0, 0, 0, 0], [6, 4, 1, 0, 0, 24], [1, 2, 0, 1, 0, 6], [-1, 1, 0, 0, 1, 1]]
basic_vars = [0, 3, 4, 5]

# print(next_simplex_sol(basic_vars, matrix, True))
all_stack_start.solve_linear_programming(basic_vars, matrix, True)