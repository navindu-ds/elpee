from elpee.utils.protocols.lp_problem import LPProblem

def check_artificial_basic_vars(problem: LPProblem):
        """
        Checks if the optimal solution obtained has artificials variables remaining as basic variables
        Returns TRUE when there is at least one artificial basic variable
        Returns FALSE when no artificial basic variables present  
        """
        artificials_idx_start = problem.n_decision_vars + problem.n_slack_vars + 1
        return not(all([problem.basic_vars[i] < artificials_idx_start for i in range(len(problem.basic_vars))]))