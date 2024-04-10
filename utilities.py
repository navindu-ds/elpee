from DualSimplexSolver import DualSimplexSolver
from LPProblem import LPProblem
from dual_simplex import dual_simplex
from sympy import Symbol, preorder_traversal, Float

DECIMALS = 3

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
    # Consider as infinity for rows with non-positive ratios
    M = 1000000
    
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

    # substitute big M with a very large number before doing ordering
    obj_row_copy = subsitute_big_M_for_row(obj_row)

    if sum(1 for elem in obj_row_copy if elem < 0) <= len(blocked_cols):
        return -1

    sorted_idx = sorted(range(len(obj_row_copy)), key=lambda k: obj_row_copy[k])
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

# XXX to be deprecated as old version
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

# TODO to be used as new implementation
def get_feasible(problem:LPProblem):
    """
    Applies the functionalities for correcting the matrix table to obtain feasibility
    If no feasible solution exists --> return None
    """
    ds_solver = DualSimplexSolver(problem)
    if not(check_feasible_positive_sol(problem.matrix)):
        problem.basic_vars, problem.matrix = ds_solver.solver()
        if problem.matrix == None:
            return None, None

    problem.matrix =  fix_feasible_0_1_pattern(problem.basic_vars, problem.matrix)
    return problem.basic_vars, problem.matrix

def get_subsets(main_list):
    """
    Returns a list of subsets of the given list
    Returns as a list of lists
    """
    if len(main_list) == 0:
        # Base case: empty list has one subset - itself
        return [[]]  
    else:
        # Recrusively generate subsets without the last element
        subsets = get_subsets(main_list[:-1]) 
        last_element = main_list[-1] 
        # Add last element to each subset generated for smaller list
        new_subsets = [subset + [last_element] for subset in subsets] 
        # Combine all subsets 
        return subsets + new_subsets  
    
def convert_num_to_padded_text(row, width, decimals):
    """
    For a given row (list of numbers/algebraic expressions) will round off 
    and add padded text to the expression for the purpose of printing
    """
    padded_row = []
    for num in row:
        # check if number is from sympy class
        if not (isinstance(num, int)) | (isinstance(num, float)):
            # if from sympy class, identify if have algebraic terms
            if num.free_symbols:
                # round of the algebraic expression and add padded text to expression
                rounded_expr = str(round_off_expr_coefficients(num)).center(width)
                padded_row.append(rounded_expr)
                continue
            else:
                # if sympy class variable is a pure number, convert into python integer or float
                num = eval(str(num))
        # round off the number and add padded text
        padded_row.append(str(round(num,decimals)).center(width))
            
    return padded_row

def subsitute_big_M_for_row(row):
    """
    Apply substitution to big M as 1,000,000 for given row
    Returns the row with substituted values
    """
    M = Symbol('M')
    row_copy = row.copy()
    for i in range(len(row_copy)):
        num = row_copy[i]
        # apply substitution only if number is not an integer or float
        if not (isinstance(num, int)) | (isinstance(num, float)):
            row_copy[i] = num.subs({M:1000000})
    return row_copy

def round_off_expr_coefficients(expression):
    """
    Rounding off the coefficients and numeric numbers in the algebraic expression
    Returns the rounded off expression
    """
    rounded_expression = expression
    for a in preorder_traversal(expression):
        if isinstance(a, Float):
            rounded_expression = rounded_expression.subs(a, round(a, 2))
    return rounded_expression

def round_off_simplex_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            elem = matrix[i][j]
            if (isinstance(elem, int)) | (isinstance(elem, float)):
                matrix[i][j] = round(elem, DECIMALS)
    return matrix