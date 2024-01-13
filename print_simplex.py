WIDTH = 12
DECIMALS = 3

# creates the list of variables including
    # objective, decision, slack and artificial variables
def get_var_list(n_decision_vars, n_slack_vars, n_artificials):
    var_names = ['P'.center(WIDTH)]
    for i in range(n_decision_vars):
        var_names.append(("X"+str(i+1)).center(WIDTH))
    for i in range(n_slack_vars):
        var_names.append(("S"+str(i+1)).center(WIDTH))
    for i in range(n_artificials):
        var_names.append(("A"+str(i+1)).center(WIDTH))
    var_names.append("Sol".center(WIDTH))
    return var_names

# generates the simplex table in user friendly manner on command line prompt into list of text
def get_simplex_table_text(basic_vars, matrix, n_decision_vars, is_max, n_artificials=0):
    n_constraints = len(matrix) - 1
    n_slack_vars = len(matrix[0]) - 1 - n_decision_vars - n_artificials
    var_names = get_var_list(n_decision_vars, n_slack_vars, n_artificials)

    rows_list = []

    # prepare first row
    if is_max:
        head_simplex_row = "MAX".center(WIDTH)
    else:
        head_simplex_row = "MIN".center(WIDTH)
    head_simplex_row += "".join(map(str, var_names[1:]))
    rows_list.append(head_simplex_row)

    # for other rows representing constraint rows
    for i in range(n_constraints+1):
        simplex_row = var_names[basic_vars[i]].ljust(WIDTH)
        matrix_row_str = [str(round(n,DECIMALS)).center(WIDTH) for n in matrix[i]]
        simplex_row += "".join(map(str, matrix_row_str))
        rows_list.append(simplex_row)
    
    # return the list of rows saved as text
    return rows_list

# prints the simplex table on the command line interface
def print_simplex_table_cli(basic_vars, matrix, n_decision_vars, is_max, n_artificials=0):
    rows_list = get_simplex_table_text(basic_vars, matrix, n_decision_vars, is_max, n_artificials)
    for row in rows_list:
        print(row)
