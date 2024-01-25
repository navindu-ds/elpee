from dual_simplex import dual_simplex

M = 1000000

def check_0_1_pattern(basic_vars, matrix):
    """
    Criteria 2 for feasibility
    Checks if the columns that correspond to the basic variables of the matrix contains the 0-1 pattern
    where the column has all zeros except at the row of the same basic variable
        i.e. matrix[basic_var][basic_var] = 1
        else for each row, matrix[row][basic_var] = 0
    If returns false --> requires to fix the pattern using linear algebraic row operations
    """
    for i, var in enumerate(basic_vars[1:]):
        column = [row[var-1] for row in matrix]

        if column[i+1] != 1 or (column.count(0) != (len(column) -1)):
            return False
    return True

def check_feasible_positive_sol(matrix):
    """
    Criteria 1 for feasibility
    Checks feasibility of matrix by checking the if the solution is positive for the constraint rows (not the objective row)
    If returns false --> matrix requires dual simplex handling 
    """
    n_rows = len(matrix)

    for i in range(1, n_rows):
        if matrix[i][-1] < 0:
            return False

    return True

def is_feasible(basic_vars, matrix):
    """
    Checks overall feasibility of the matrix based on the 2 criteria
    """
    if check_feasible_positive_sol(matrix):
        if check_0_1_pattern(basic_vars, matrix):
            return True
    return False

def create_ratio_col(matrix, pivot_col_var):
    """
    Creates the ratio column = Solution column / pivot column
    For ratio values that are zero, negative or infinity will be taken as M 
    """
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

def select_pivot_col(obj_row, is_max, blocked_cols):
    """
    If the matrix is not positive, selects a pivot column to find the entering variable
    Returns the basic variable column number that is not blocked
        Blocked columns are used to indicate any columns that were used as entering variable unsuccessfully
    If no such column that can be used returns -1 
    """
    # For minimization problems will take the opposite signs to allow to select the largest positive number
    if not(is_max):
        obj_row = [element * -1 for element in obj_row]

    if sum(1 for elem in obj_row if elem < 0) <= len(blocked_cols):
        return -1

    sorted_idx = sorted(range(len(obj_row)), key=lambda k: obj_row[k])
    for n in sorted_idx:
        pivot_col_var = n + 1
        if pivot_col_var not in blocked_cols:
            return pivot_col_var
    
    return -1

def fix_feasible_0_1_pattern(basic_vars, matrix):
    """
    Function to fix the 0-1 pattern for columns of basic variables
    Does scaled multiplication to the row of the basic variable if matrix[basic_var][basic_var] != 1
    Does scaled addition of the basic variable row onto rows where matrix[row][basic_var] != 0
    """
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

def get_feasible(basic_vars, matrix):
    """
    Applies the functionalities for correcting the matrix table to obtain feasibility
    If no feasible solution exists --> return None
    """
    if not(check_feasible_positive_sol(matrix)):
        basic_vars, matrix = dual_simplex(basic_vars, matrix)
        if matrix == None:
            return None, None

    matrix =  fix_feasible_0_1_pattern(basic_vars, matrix)
    return basic_vars, matrix