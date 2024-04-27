from elpee.utils.FeasibleHandler import FeasibleHandler
from elpee import LPProblem
from elpee.utils.SimplexPrinter import SimplexPrinter
from elpee.utils.utilities import create_ratio_col, get_subsets

class AlternateSolver():
    """
    A class to find and generate alternate solutions for the given optimal problems
    
    The given problem should be optimized

    Attributes
    ----------
    problem : elpee.LPProblem
        The optimized problem given to find alternate solutions
    n_alternates : int
        Number of alternate solutions available for given optimal LPProblem
    simplex_printer : elpee.utils.SimplexPrinter 
        An instance of printer to visualize the simplex table
        of given LP problem
    feasible_handler : elpee.utils.FeasibleHandler
        An instance of handler object to retain feasibility of
        LP problem and its solutions

    Methods
    -------
    check_alternate_solutions() -> bool
        Returns True/False if any alternate solutions are present
    extract_alternate_solution(version_num) -> elpee.LPProblem
        Returns one of the alternate solutions. Version num is in the range of
        1 to n_alternates inclusive
    display_all_alternate_solutions() -> None
        Displays all alternate solutions for given optimal problem
    """
    def __init__(self, problem:LPProblem):
        self.problem = problem
        self.printer = SimplexPrinter()
        self.feasible_handler = FeasibleHandler()
        self.n_alternates = len(self.__get_alterations_combo_list())
        self.__update_num_alternates()

    def __update_num_alternates(self):
        self.problem.set_num_alternates(self.n_alternates)
    
    def check_alternate_solutions(self):
        """
        Checks if the given problem has alternate solutions

        Return
        ------
        True/False  
        """
        # Checks if the simplex matrix has any alternate optimal solutions
        # Compares and checks if there are higher number of zeros in the objective row
        # Returns True when there are alternative optimal solutions
        num_zeros = self.problem.obj_row.count(0)
        if num_zeros > self.problem.n_constraints:
            return True
        elif num_zeros == self.problem.n_constraints:
            return False
        else:
            print("\nSolution not optimal")
            return False
        
    def __get_entering_cols_for_alternates(self):
        """
        Returns a list of columns that can be used to create alternative optimal solutions
        Returns a list of column indexes with 0 in the objective row except in basic variable columns
        """
        cols_for_alternates = []
        for i in range(len(self.problem.obj_row)):
            if i+1 not in self.problem.basic_vars:
                if self.problem.obj_row[i] == 0:
                    cols_for_alternates.append(i+1)
        return cols_for_alternates
    
    def __apply_simplex_update(self, pivot_col_var):
        """
        Applies simplex update for the given pivot col to get an updated simplex table
        Returns updated basic_vars list and matrix
        """
        M = 1000000
        
        new_var_name = self.printer.print_var_name(pivot_col_var, self.problem)
        # create a ratio column for the pivot col provided
        ratio_col = create_ratio_col(self.problem.matrix, pivot_col_var)
        if min(ratio_col) == M:
            return None, None
        else:
            # selecting the leaving variable
            pivot_row = ratio_col.index(min(ratio_col)) + 1
        pivot_row_name = self.printer.print_var_name(self.problem.basic_vars[pivot_row], self.problem)
        print(f"Taking {pivot_row_name} = 0 for & setting {new_var_name} as a Basic Variable for the alternate solution")
        # make the change in basic variables list
        self.problem.basic_vars[pivot_row] = pivot_col_var
        
        # apply feasibility fixes for the matrix with basic variables updated
        self.problem = self.feasible_handler.get_feasible(self.problem)
        if self.problem.matrix == None: 
            return None, None
        
        # return the updated basic_vars, matrix after simplex updates
        return self.problem.basic_vars, self.problem.matrix
    
    def __get_alternate_solutions(self, alteration_combo):
        """
        For a given set of columns for which an alternate solution can be derived,
        apply simplex updates to all the columns provided in alteration combo list and prints final alternate solution
        """
        for pivot_col in alteration_combo:
            self.problem.basic_vars, self.problem.matrix = self.__apply_simplex_update(pivot_col)
            if self.problem.matrix == None:
                print("\nFeasible alternate solution not found")
                return None, None
        # print the final alternate solution based on set of columns provided
        self.printer.print_simplex_table_cli(self.problem)
    
    def __get_alterations_combo_list(self):
        # obtain list of variables for generating alternate solutions
        alternate_cols = self.__get_entering_cols_for_alternates()
        # obtain a list of combinations of columns for creating all possible alternate solutions
            # exclude the null set when extracting the subsets
        alterations_combo_list = get_subsets(alternate_cols)[1:]
        return alterations_combo_list

    def extract_alternate_solution(self, version_num):
        """
        Extracts an alternate solution based on version_num provided 

        Parameters
        ----------
        version_num : int
            index of the alternate solution to generate in the range 1 to num_alternates
        
        Return
        ------
        elpee.LPProblem containing alternate solution based on given index
        """
        if not self.problem.is_optimal:
            print(f"\nGiven problem is not optimal. No alternate solutions exist.")
            return None

        if self.problem.num_alternates != 0:
            alterations_combo_list = self.__get_alterations_combo_list()

            if version_num <= len(alterations_combo_list):
                print(f"\nAlternate Solution #{version_num}")
                self.__get_alternate_solutions(alterations_combo_list[version_num-1])
                return self.problem
            else:
                print(f"\nThere are only {len(alterations_combo_list)} versions for Alternate Solutions!")
                print(f"Cannot return Alternate Solution #{version_num}")
                return None
        else:
            print("There are no alternate solutions!")
            return None
        
    def display_all_alternate_solutions(self):
        """
        Display all alternate solutions for given optimal problem
        """
        
        print("\nDisplaying all Alternate Optimal Solutions for Simplex Table Provided...")

        if not self.problem.is_optimal:
            print("\nGiven problem is not optimal. No alternate solutions exist.")
        else:
            if self.problem.num_alternates != 0:
                alterations_combo_list = self.__get_alterations_combo_list()
                initial_problem = self.problem.copy()

                for i, alteration_combo in enumerate(alterations_combo_list):
                    print(f"\nAlternate Solution #{i+1}")
                    self.__get_alternate_solutions(alteration_combo)

                    self.problem = initial_problem
            else:
                print("\nThere are no alternate solutions to display!")