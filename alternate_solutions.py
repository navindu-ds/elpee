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
