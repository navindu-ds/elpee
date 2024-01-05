from dual_simplex import dual_simplex
from print_simplex import print_simplex_table_cli

M = 1000000

def check_feasible_positive_sol(matrix):
    n_rows = len(matrix)
    dual_simplex_flag = False

    for i in range(1, n_rows):
        if matrix[i][-1] < 0:
            dual_simplex_flag = True
            break

    return dual_simplex_flag

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
            if ratio_col[row_i-1] < 0:
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
            print("Cannot be optimized")
            return basic_vars, matrix
        ratio_col = create_ratio_col(matrix, pivot_col_var)
        if min(ratio_col) == M:
            blocked_cols.append(pivot_col_var)
        else:
            pivot_row_var = ratio_col.index(min(ratio_col)) + 1
            break
    basic_vars[pivot_row_var] = pivot_col_var
    return basic_vars, matrix

def get_feasible(basic_vars, matrix, n_decision_vars, is_max):
    
    if check_feasible_positive_sol(matrix):
        basic_vars, matrix = dual_simplex(basic_vars, matrix)

    matrix =  fix_feasible_0_1_pattern(basic_vars, matrix)

    return matrix

def solve_linear_programming(basic_vars, matrix, n_decision_vars, is_max):

    feasible_count = 1
    
    while check_feasible_positive_sol(matrix):
        print("\n...Generating Initial Feasible Solution for")
        print_simplex_table_cli(basic_vars, matrix, n_decision_vars, is_max)
        matrix = get_feasible(basic_vars, matrix, n_decision_vars, is_max)

    print(f"\nFeasible Solution # {feasible_count}")
    print_simplex_table_cli(basic_vars, matrix, n_decision_vars, is_max)

    while(not(check_optimal(matrix[0][:-1], is_max))):
        feasible_count += 1
        basic_vars, matrix = optimize(basic_vars, matrix, is_max)
        matrix = get_feasible(basic_vars, matrix, n_decision_vars, is_max)
        print(f"\nFeasible Solution # {feasible_count}")
        print_simplex_table_cli(basic_vars, matrix, n_decision_vars, is_max)

    print("\nOptimized!")
