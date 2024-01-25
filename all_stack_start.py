from dual_simplex import dual_simplex
from print_simplex import print_simplex_table_cli, print_entering_leaving_vars, print_var_name
from bigM_handler import check_artificial_basic_vars
from alternate_solutions import check_alternate_solutions, get_entering_cols_for_alternates, get_alternate_solutions
from utilities import create_ratio_col, is_feasible, get_feasible, select_pivot_col

M = 1000000

def is_optimal(obj_row, is_max):
    """
    Returns true if the objective row of the matrix (first row without solution value) indicates optimal solution 
    """
    if is_max:
        # for maximization, all coefficients of objective row should be non-negative
        return all(element >= 0 for element in obj_row)
    else:
        # for minimization, all coefficients of objective row should be non-positive
        return all(element <= 0 for element in obj_row)

def optimize(basic_vars, matrix, is_max):
    """
    Core function for optimizing the matrix by changing the basic variables
    When matrix cannot be optimized will return None
    """
    obj_row = matrix[0][:-1]
    n_cols = len(obj_row)
    blocked_cols = []
    while len(blocked_cols) < n_cols:
        pivot_col_var = select_pivot_col(obj_row, is_max, blocked_cols)
        if pivot_col_var == -1:
            # No suitable pivot column available
            print("\nNo suitable entering varaible for selection")
            return None, None
        ratio_col = create_ratio_col(matrix, pivot_col_var)
        if min(ratio_col) == M:
            # invalid ratio column with no suitable selections to be made
            # will block the pivot col from being selected again 
            # and find an alternate entering variable
            blocked_cols.append(pivot_col_var)
        else:
            # leaving varaible identified
            pivot_row_var = ratio_col.index(min(ratio_col)) + 1
            break
    basic_vars[pivot_row_var] = pivot_col_var
    return basic_vars, matrix

def solve_linear_programming(basic_vars, matrix, n_decision_vars, is_max, n_artificials=0):
    """
    Main executing function to run the linear programming methodology for 
    all stack starting and dual simplex methods 
    """
    n_slack_vars = len(matrix[0][:-1]) - n_decision_vars - n_artificials 
    feasible_count = 1

    while not(is_feasible(basic_vars, matrix)):
        print("\n...Generating Initial Feasible Solution for")
        print_simplex_table_cli(basic_vars, matrix, n_decision_vars, is_max, n_artificials)
        old_basic_vars = basic_vars.copy()
        basic_vars, matrix = get_feasible(basic_vars, matrix)
        if matrix == None:
            print("\nNo feasible solution found")
            return
        print_entering_leaving_vars(old_basic_vars, basic_vars, n_decision_vars, n_slack_vars, n_artificials)
        
    print(f"\nFeasible Solution # {feasible_count}")
    print_simplex_table_cli(basic_vars, matrix, n_decision_vars, is_max, n_artificials)
    
    while not(is_optimal(matrix[0][:-1], is_max)):
        feasible_count += 1
        old_basic_vars = basic_vars.copy()
        basic_vars, matrix = optimize(basic_vars, matrix, is_max)
        if matrix == None:
            print("\nCannot be optimized further")
            return 
        print_entering_leaving_vars(old_basic_vars, basic_vars, n_decision_vars, n_slack_vars, n_artificials)
        old_basic_vars = basic_vars.copy()
        basic_vars, matrix = get_feasible(basic_vars, matrix)
        if matrix == None:
            print("\nNo further feasible solution found")
            return 
        print_entering_leaving_vars(old_basic_vars, basic_vars, n_decision_vars, n_slack_vars, n_artificials)
        print(f"\nFeasible Solution # {feasible_count}")
        print_simplex_table_cli(basic_vars, matrix, n_decision_vars, is_max, n_artificials)
    
    if (check_artificial_basic_vars(basic_vars, matrix[0][:-1], n_decision_vars, n_artificials)):
        print("\nArtificial variables found in optimal soltion.\nProblem is infeasible.")
        return None
    else:
        print("\nOptimized Solution Received!")

    if check_alternate_solutions(matrix[0][:-1], len(matrix)-1):
        print("\nThere are Alternate Optimal Solutions")
        alternate_cols = get_entering_cols_for_alternates(basic_vars, matrix[0][:-1])
        for i, col in enumerate(alternate_cols):
            var_name = print_var_name(col, n_decision_vars, n_slack_vars, n_artificials)
            print(f"{i+1}. Taking {var_name} as a Basic Variable will return an alternate solution")