from elpee.utils.utilities import create_ratio_col, get_feasible, get_subsets
from print_simplex import print_var_name, print_simplex_table_cli

def check_alternate_solutions(obj_row, n_constraints):
    """
    Checks if the simplex matrix has any alternate optimal solutions
    Compares and checks if there are higher number of zeros in the objective row
    Returns True when there are alternative optimal solutions
    """
    num_zeros = obj_row.count(0)
    if num_zeros > n_constraints:
        return True
    elif num_zeros == n_constraints:
        return False
    else:
        print("\nSolution not optimal")
        return False
    
def get_entering_cols_for_alternates(basic_vars, obj_row):
    """
    Returns a list of columns that can be used to create alternative optimal solutions
    Returns a list of column indexes with 0 in the objective row except in basic variable columns
    """
    cols_for_alternates = []
    for i in range(len(obj_row)):
        if i+1 not in basic_vars:
            if obj_row[i] == 0:
                cols_for_alternates.append(i+1)
    return cols_for_alternates

def apply_simplex_update(basic_vars, matrix, pivot_col_var, n_decision_vars, n_slack_vars, n_artificials=0):
    """
    Applies simplex update for the given pivot col to get an updated simplex table
    Returns updated basic_vars list and matrix
    """
    M = 1000000
    
    new_var_name = print_var_name(pivot_col_var, n_decision_vars, n_slack_vars, n_artificials)
    # create a ratio column for the pivot col provided
    ratio_col = create_ratio_col(matrix, pivot_col_var)
    if min(ratio_col) == M:
        return None, None
    else:
        # selecting the leaving variable
        pivot_row = ratio_col.index(min(ratio_col)) + 1
    pivot_row_name = print_var_name(basic_vars[pivot_row], n_decision_vars, n_slack_vars, n_artificials)
    print(f"Taking {pivot_row_name} = 0 for & setting {new_var_name} as a Basic Variable for the alternate solution")
    # make the change in basic variables list
    basic_vars[pivot_row] = pivot_col_var
    
    # apply feasibility fixes for the matrix with basic variables updated
    basic_vars, matrix = get_feasible(basic_vars, matrix)
    if matrix == None:
        return None, None
    
    # return the updated basic_vars, matrix after simplex updates
    return basic_vars, matrix

def get_alternate_solutions(basic_vars, matrix, is_max, alteration_combo, n_decision_vars, n_slack_vars, n_artificials=0):
    """
    For a given set of columns for which an alternate solution can be derived,
    apply simplex updates to all the columns provided in alteration combo list and prints final alternate solution
    """
    for col in alteration_combo:
        basic_vars, matrix = apply_simplex_update(basic_vars, matrix, col, n_decision_vars, n_slack_vars, n_artificials)
        if matrix == None:
            print("\nFeasible alternate solution not found")
            return None, None
    # print the final alternate solution based on set of columns provided
    print_simplex_table_cli(basic_vars, matrix, n_decision_vars, is_max, n_artificials)
    return basic_vars, matrix

def extract_alternate_solution(version_num, basic_vars, matrix, is_max, n_decision_vars, n_artificials=0):
    """
    Extracts an alternate solution based on version_num provided 
    """
    n_slack_vars = len(matrix[0][:-1]) - n_decision_vars - n_artificials 

    if check_alternate_solutions(matrix[0][:-1], len(matrix)-1):
        # obtain list of variables for generating alternate solutions
        alternate_cols = get_entering_cols_for_alternates(basic_vars, matrix[0][:-1])
        # obtain a list of combinations of columns for creating all possible alternate solutions
            # exclude the null set when extracting the subsets
        alterations_combo_list = get_subsets(alternate_cols)[1:]

        if version_num <= len(alterations_combo_list):
            print(f"\nAlternate Solution #{version_num}")
            basic_vars, matrix = get_alternate_solutions(basic_vars, matrix, is_max, alterations_combo_list[version_num-1], n_decision_vars, n_slack_vars, n_artificials)
            return basic_vars, matrix
        else:
            print(f"\nThere are only {len(alterations_combo_list)} versions for Alternate Solutions!")
            print(f"Cannot return Alternate Solution #{version_num}")
            return None, None
    else:
        print("There are no alternate solutions!")
        return None, None
    
def display_all_alternate_solutions(basic_vars, matrix, is_max, n_decision_vars, n_artificials=0):
    print("\nDisplaying all Alternate Optimal Solutions for Simplex Table Provided...")
    n_slack_vars = len(matrix[0][:-1]) - n_decision_vars - n_artificials 

    if check_alternate_solutions(matrix[0][:-1], len(matrix)-1):
        # obtain list of variables for generating alternate solutions
        alternate_cols = get_entering_cols_for_alternates(basic_vars, matrix[0][:-1])
        # obtain a list of combinations of columns for creating all possible alternate solutions
            # exclude the null set when extracting the subsets
        alterations_combo_list = get_subsets(alternate_cols)[1:]

        for i, alteration_combo in enumerate(alterations_combo_list):
            print(f"\nAlternate Solution #{i+1}")

            new_basic_vars = basic_vars.copy()
            new_matrix = matrix.copy()

            get_alternate_solutions(new_basic_vars, new_matrix, is_max, alteration_combo, n_decision_vars, n_slack_vars, n_artificials)
    else:
        print("\nThere are no alternate solutions to display!")