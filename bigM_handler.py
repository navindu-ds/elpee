def check_artificial_basic_vars(basic_vars, obj_row, n_decision_vars, n_artificials):
    """
    Checks if the optimal solution obtained has artificials variables remaining as basic variables
    Returns TRUE when there is at least one artificial basic variable
    Returns FALSE when no artificial basic variables present  
    """
    n_slack_vars = len(obj_row) - n_artificials - n_decision_vars
    artificials_idx_start = n_decision_vars + n_slack_vars + 1
    return not(all([basic_vars[i] < artificials_idx_start for i in range(len(basic_vars))]))
