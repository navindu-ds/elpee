from dual_simplex import dual_simplex
from print_simplex import print_simplex_table_cli

M = 1000000

def check_feasible_positive_sol(matrix):
    n_rows = len(matrix)

    for i in range(1, n_rows):
        if matrix[i][-1] < 0:
            return False

    return True

def check_feasibility(basic_vars, matrix):
    if check_feasible_positive_sol(matrix):
        if check_0_1_pattern(basic_vars, matrix):
            return True
    return False

def check_0_1_pattern(basic_vars, matrix):
    for i, var in enumerate(basic_vars[1:]):
        print(var)
        column = [row[var-1] for row in matrix]
        print(column)

        if column[i+1] != 1 or (column.count(0) != (len(column) -1)):
            return False
    return True

def fix_feasible_0_1_pattern(basic_vars, matrix):
    n_rows = len(matrix)
    for row_i ,basic_var in enumerate(basic_vars):
        # no need to check 0-1 pattern for objective variable
        if basic_var == 0:
            continue

        # checking and fixing basic variables coefficient into 1
        if matrix[row_i][basic_var-1] != 1:
            matrix[row_i] = [element / matrix[row_i][basic_var-1] for element in matrix[row_i]]

        # checking if zeros are maintained for 0-1 pattern
        for i in range(n_rows):
            # except for row with the basic variable
            if i != row_i:  
                if matrix[i][basic_var-1] != 0:
                    scaled_piv_row = [element * matrix[i][basic_var-1] for element in matrix[row_i]]
                    matrix[i] = [a-b for a,b in zip(matrix[i], scaled_piv_row)]
        
    return matrix

def check_optimal(obj_row, is_max):
    is_optimal = False
    if is_max:
        is_optimal = all(element >= 0 for element in obj_row)
    else:
        is_optimal = all(element <= 0 for element in obj_row)
    return is_optimal

def select_pivot_col(obj_row, is_max, blocked_cols):
    if not(is_max):
        obj_row = [element * -1 for element in obj_row]

    for _ in range(len(obj_row)):

        pivot_col_var = obj_row.index(min(obj_row)) + 1

        if pivot_col_var not in blocked_cols:
            return pivot_col_var
    
    return -1

def create_ratio_col(matrix, pivot_col_var):
    n_rows = len(matrix)
    ratio_col = [0]*(n_rows-1)
    for row_i in range(1, n_rows):
        if matrix[row_i][pivot_col_var-1] != 0:
            ratio_col[row_i-1] = matrix[row_i][-1] / matrix[row_i][pivot_col_var-1]
            if ratio_col[row_i-1] <= 0:
                ratio_col[row_i-1] = M
        else:
            ratio_col[row_i-1] = M
    return ratio_col

def optimize(basic_vars, matrix, is_max):
    obj_row = matrix[0][:-1]
    n_cols = len(obj_row)
    blocked_cols = []
    while len(blocked_cols) < n_cols:
        pivot_col_var = select_pivot_col(obj_row, is_max, blocked_cols)
        if pivot_col_var == -1:
            return False, None, None
        ratio_col = create_ratio_col(matrix, pivot_col_var)
        if min(ratio_col) == M:
            blocked_cols.append(pivot_col_var)
        else:
            pivot_row_var = ratio_col.index(min(ratio_col)) + 1
            break
    basic_vars[pivot_row_var] = pivot_col_var
    return True, basic_vars, matrix

def get_feasible(basic_vars, matrix, n_decision_vars, is_max):
    
    if not(check_feasible_positive_sol(matrix)):
        is_dual_simplexed, basic_vars, matrix = dual_simplex(basic_vars, matrix)
        if not(is_dual_simplexed):
            return False, None

    matrix =  fix_feasible_0_1_pattern(basic_vars, matrix)

    return True, matrix

def solve_linear_programming(basic_vars, matrix, n_decision_vars, is_max):

    feasible_count = 1
    
    while not(check_feasible_positive_sol(matrix)):
        print("\n...Generating Initial Feasible Solution for")
        print_simplex_table_cli(basic_vars, matrix, n_decision_vars, is_max)
        is_feasible, matrix = get_feasible(basic_vars, matrix, n_decision_vars, is_max)
        if not(is_feasible):
            print("\nNo feasible solution found")
            return

    print(f"\nFeasible Solution # {feasible_count}")
    print_simplex_table_cli(basic_vars, matrix, n_decision_vars, is_max)

    is_optimizable = True
    while(not(check_optimal(matrix[0][:-1], is_max))):
        feasible_count += 1
        is_optimizable, basic_vars, matrix = optimize(basic_vars, matrix, is_max)
        if not(is_optimizable):
            print("\nCannot be optimized further")
            break
        is_feasible, matrix = get_feasible(basic_vars, matrix, n_decision_vars, is_max)
        if not(is_feasible):
            print("\nNo further feasible solution found")
            return
        print(f"\nFeasible Solution # {feasible_count}")
        print_simplex_table_cli(basic_vars, matrix, n_decision_vars, is_max)

    if is_optimizable:
        print("\nOptimized Solution Received!")

# column = [0,1,0,0,0]
# x=3
# if column[x] == 1 and column.count(0) == (len(column) -1):
#     print("Yay")
# else:
#     print("Noo")

# matrix = [[ 0, 13/7, 0, 71/7, -2/7, 0, 10/7, 970/7],
#           [ 1,  5/7, 0, -5/7, 10/7, 0, -1/7,  50/7],
#           [ 0, -6/7, 0, 13/7,-61/7, 1,  4/7, 325/7],
#           [ 0,  2/7, 1, 12/7, -3/7, 0,  1/7,  55/7]]
# basic_vars = [0, 1, 6, 3]
# n_decision_vars = 4

# matrix = [[0, 0, 1, 0, 0, 15],
#           [1, 1, 1,-1, 0,  5],
#           [1, 0, 0, 1, 0, 10],
#           [0, 0,-1, 1, 1,  5]]
# basic_vars = [0, 2, 1, 5]
# n_decision_vars = 2
# print(check_feasibility(basic_vars, matrix))