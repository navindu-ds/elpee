M = 1000000

def select_pivot_col(ratio_row, blocked_cols):
    """
    Selects the pivot column based on ratio row and not in blocked list
    """
    sorted_idx = sorted(range(len(ratio_row)), key=lambda k: ratio_row[k])
    for n in sorted_idx:
        pivot_col_var = n + 1
        if pivot_col_var not in blocked_cols:
            return pivot_col_var
    print("\nNo suitable pivot column - Choosing another pivot row")
    return -1

def select_pivot_row(basic_vars, matrix, blocked_rows):
    """
    Selects the appropriate pivot row that has a negative solution value and not in blocked list
    """
    sol_col = []
    neg_sol = 0
    for i, row in enumerate(matrix):
        if i !=0:
            sol_col.append(row[-1])
            if row[-1] < 0:
                neg_sol += 1
    sorted_idx = sorted(range(len(sol_col)), key=lambda k: sol_col[k])
    
    for i in range(neg_sol):
        if basic_vars[sorted_idx[i]+1] not in blocked_rows:
            return sorted_idx[i]+1
    print("\nNo suitable pivot row - Cannot make feasible solution")
    return -1
        
def create_ratio_row(matrix, pivot_row, pivot_row_var):
    """
    Creates the ratio row given the selected pivot row as 
        absolute value of (objective_row / pivot row)
    Marks 0 and infinity ratios as M
    """
    obj_row = matrix[0][:-1]
    ratio_row = [0]*len(obj_row)
    for i in range(len(obj_row)):
        if matrix[pivot_row][i] == 0:
            ratio_row[i] = M
        elif obj_row[i] == 0:
            ratio_row[i] = M
        else:
            ratio_row[i] = abs(obj_row[i] / matrix[pivot_row][i])
    ratio_row[pivot_row_var-1] = M
    return ratio_row
        
def dual_simplex(basic_vars, matrix):
    """
    Main executing function to execute dual simplex adjustments to the simplex matrix
    """
    blocked_rows = []
    n_rows = len(matrix)
    n_cols = len(matrix[0][:-1])
    while len(blocked_rows) < n_rows:
        pivot_row = select_pivot_row(basic_vars, matrix, blocked_rows)
        if pivot_row == -1:
            # print("\nNo further feasible solution")
            return None, None
        pivot_row_var = basic_vars[pivot_row]

        blocked_cols = []

        ratio_row = create_ratio_row(matrix, pivot_row, pivot_row_var)
        
        j = 1
        while (j <= n_cols) & (sorted(ratio_row)[j-1] != M): 
            pivot_col_var = select_pivot_col(ratio_row, blocked_cols)
            if pivot_col_var != -1:
                pivot_cell = matrix[pivot_row][pivot_col_var-1]
                if pivot_cell > 0:
                    blocked_cols.append(pivot_col_var)
                    j += 1
                else:
                    basic_vars[pivot_row] = pivot_col_var
                    return basic_vars, matrix
            else:
                continue
        blocked_rows.append(pivot_row)
    # print("\nNo further feasible solution")
    return None, None
