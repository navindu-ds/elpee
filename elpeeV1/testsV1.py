import all_stack_start
M = 1000000

def test_solver01():

    matrix = [[-5, -4, 0, 0,  0], 
              [ 6,  4, 1, 0, 24], 
              [ 1,  2, 0, 1,  6]]
    basic_vars = [0, 3, 4]
    n_decision_vars = 2
    is_max = True
    n_artificials = 0

    output_matrix = [[0, 0,  0.75 ,  0.5, 21 ],
                     [1, 0,  0.25 , -0.5,  3 ],
                     [0, 1, -0.125,  0.75,  1.5]]
    output_basic_vars = [0, 1, 2]

    assert (output_basic_vars, output_matrix) == all_stack_start.solve_linear_programming(basic_vars, matrix, n_decision_vars, is_max, n_artificials)

def test_solver02():

    matrix = [[-5, -4, 0, 0, 0,  0], 
              [ 6,  4, 1, 0, 0, 24], 
              [ 1,  2, 0, 1, 0,  6], 
              [-1,  1, 0, 0, 1,  1]]
    basic_vars = [0, 3, 4, 5]
    n_decision_vars = 2
    is_max = True
    n_artificials = 0

    output_matrix = [[0.0, 0.0, 0.75, 0.5, 0.0, 21.0], 
                     [1.0, 0.0, 0.25, -0.5, 0.0, 3.0], 
                     [0.0, 1.0, -0.125, 0.75, 0.0, 1.5], 
                     [0.0, 0.0, 0.375, -1.25, 1.0, 2.5]]
    output_basic_vars = [0, 1, 2, 5]

    assert (output_basic_vars, output_matrix) == all_stack_start.solve_linear_programming(basic_vars, matrix, n_decision_vars, is_max, n_artificials)

def test_solver03():

    matrix = [[-3, 1, 0, 0, 0], 
              [ 4, -1, 1, 0, 8], 
              [-8, -1, 0, 1, -12]]
    basic_vars = [0, 3, 4]
    n_decision_vars = 2
    is_max = True
    n_artificials = 0

    output_matrix = [[0.0, 0.25, 0.75, 0.0, 6.0], 
                     [0.0, -3.0, 2.0, 1.0, 4.0], 
                     [1.0, -0.25, 0.25, 0.0, 2.0]]
    output_basic_vars = [0, 4, 1]

    assert (output_basic_vars, output_matrix) == all_stack_start.solve_linear_programming(basic_vars, matrix, n_decision_vars, is_max, n_artificials)

def test_solver04():

    matrix = [[-19,-13,-12,-17,  0,  0,  0,  0],
              [  3,  2,  1,  2,  1,  0,  0,225],
              [  1,  1,  1,  1,  0,  1,  0,117],
              [  4,  3,  3,  4,  0,  0,  1,420]]
    basic_vars = [0, 5, 6, 7]
    n_decision_vars = 4
    is_max = True
    n_artificials = 0

    output_matrix = [[0.0, 1.0, 0.0, 0.0, 2.0, 1.0, 3.0, 1827.0], 
                     [1.0, 1.0, 0.0, 0.0, 1.0, 2.0, -1.0, 39.0], 
                     [0.0, 1.0, 1.0, 0.0, 0.0, 4.0, -1.0, 48.0], 
                     [0.0, -1.0, 0.0, 1.0, -1.0, -5.0, 2.0, 30.0]]
    output_basic_vars = [0, 1, 3, 4]

    assert (output_basic_vars, output_matrix) == all_stack_start.solve_linear_programming(basic_vars, matrix, n_decision_vars, is_max, n_artificials)

def test_solver05():

    matrix = [[  1, -2,  1,  0,  0,  0,  0],
              [  1,  2,  1,  1,  0,  0, 12],
              [  2,  1, -1,  0,  1,  0,  6],
              [ -1,  3,  0,  0,  0,  1,  9]]
    basic_vars = [0, 4, 5, 6]
    n_decision_vars = 3
    is_max = False
    n_artificials = 0

    output_matrix = [[0.0, -4.0, 0.0, -1.0, 0.0, 0.0, -12.0], 
                     [0.0, 1.0, 1.0, 0.667, -0.333, 0.0, 6.0], 
                     [1.0, 1.0, 0.0, 0.333, 0.333, 0.0, 6.0], 
                     [0.0, 4.0, 0.0, 0.333, 0.333, 1.0, 15.0]]
    output_basic_vars = [0, 3, 1, 6]

    assert (output_basic_vars, output_matrix) == all_stack_start.solve_linear_programming(basic_vars, matrix, n_decision_vars, is_max, n_artificials)

def test_solver07():

    matrix = [[-3,  1, -1,  0,  0,  0,  0], 
              [ 4, -1,  0,  1,  0,  0,  8],
              [-8, -1, -3,  0,  1,  0,-12],
              [ 5,  0, -1,  0,  0,  1, 13]]
    basic_vars = [0, 4, 5, 6]
    n_decision_vars = 3
    is_max = False
    n_artificials = 0

    output_matrix = None
    output_basic_vars = None

    assert (output_basic_vars, output_matrix) == all_stack_start.solve_linear_programming(basic_vars, matrix, n_decision_vars, is_max, n_artificials)

def test_solver16():

    matrix = [[0, 0, 1, 0, 0, 15],
              [1, 1, 1,-1, 0,  5],
              [1, 0, 0, 1, 0, 10],
              [0, 0,-1, 1, 1,  5]]
    basic_vars = [0, 2, 1, 5]
    n_decision_vars = 2
    is_max = False
    n_artificials = 0

    output_matrix = None
    output_basic_vars = None

    assert (output_basic_vars, output_matrix) == all_stack_start.solve_linear_programming(basic_vars, matrix, n_decision_vars, is_max, n_artificials)

def test_solver17():

    matrix = [[ 0, 13/7, 0, 71/7, -2/7, 0, 10/7, 970/7],
              [ 1,  5/7, 0, -5/7, 10/7, 0, -1/7,  50/7],
              [ 0, -6/7, 0, 13/7,-61/7, 1,  4/7, 325/7],
              [ 0,  2/7, 1, 12/7, -3/7, 0,  1/7,  55/7]]
    basic_vars = [0, 1, 6, 3]
    n_decision_vars = 4
    is_max = True
    n_artificials = 0

    output_matrix = [[0.2, 2.0, 0.0, 10.0, 0.0, 0.0, 1.4, 140.0], 
                     [0.7, 0.5, 0.0, -0.5, 1.0, 0.0, -0.1, 5.0], 
                     [6.1, 3.5, 0.0, -2.5, 0.0, 1.0, -0.3, 90.0], 
                     [0.3, 0.5, 1.0, 1.5, 0.0, 0.0, 0.1, 10.0]]
    output_basic_vars = [0, 5, 6, 3]

    assert (output_basic_vars, output_matrix) == all_stack_start.solve_linear_programming(basic_vars, matrix, n_decision_vars, is_max, n_artificials)

def test_solver18():

    matrix = [[0, 0, 0, 0, 2, 1, 3, 1827],
              [1, 1, 0, 0, 1, 2,-1,   39],
              [0, 1, 1, 0, 0, 4,-1,   48],
              [0,-1, 0, 1,-1,-5, 2,   30]]
    basic_vars = [0, 1, 3, 4]
    n_decision_vars = 4
    is_max = True
    n_artificials = 0

    output_matrix = matrix.copy()
    output_basic_vars = basic_vars.copy()

    assert (output_basic_vars, output_matrix) == all_stack_start.solve_linear_programming(basic_vars, matrix, n_decision_vars, is_max, n_artificials)

def test_solver19():

    matrix = [[-1, -1, 0, 0, 0, -M, -M,  0],
              [-1,  1, 1, 0, 0,  0,  0,  2],
              [ 6,  4, 0,-1, 0,  1,  0, 24],
              [ 0,  1, 0, 0,-1,  0,  1,  1]]
    basic_vars = [0, 3, 6, 7]
    n_decision_vars = 2
    n_artificials = 2
    is_max = False

    output_matrix = [[0.0, 0.0, 0.0, -0.167, -0.333, -999999.833, -999999.667, 4.333], 
                     [0.0, 0.0, 1.0, -0.167, 1.667, 0.167, -1.667, 4.333], 
                     [1.0, 0.0, 0.0, -0.167, 0.667, 0.167, -0.667, 3.333], 
                     [0, 1, 0, 0, -1, 0, 1, 1]]
    output_basic_vars = [0, 3, 1, 2]

    assert (output_basic_vars, output_matrix) == all_stack_start.solve_linear_programming(basic_vars, matrix, n_decision_vars, is_max, n_artificials)



def test_solver21():

    matrix = [[-3,  1, -1, 0,  0, 0, M,  0],
              [ 4, -1,  0, 1,  0, 0, 0,  8],
              [ 8,  1,  3, 0, -1, 0, 1, 12],
              [ 5,  0, -1, 0,  0, 1, 0, 13]]
    basic_vars = [0, 4, 7, 6]
    n_decision_vars = 3
    n_artificials = 1
    is_max = True

    output_matrix = None
    output_basic_vars = None

    assert all_stack_start.solve_linear_programming(basic_vars, matrix, n_decision_vars, is_max, n_artificials) == (output_basic_vars, output_matrix)

def test_solver22():

    matrix = [[  1, -2,  0,  0,  0,  M,  M, 0],
              [  1,  1, -1,  0,  0,  1,  0, 2],
              [ -1,  1,  0, -1,  0,  0,  1, 1],
              [  0,  1,  0,  0,  1,  0,  0, 3]]
    basic_vars = [0, 6, 7, 5]
    n_decision_vars = 2
    n_artificials = 2
    is_max = True

    output_matrix = [[1.0, 0.0, 0.0, 0.0, 2.0, 1000000.0, 1000000.0, 6.0], 
                     [1.0, 0.0, 0.0, 1.0, 1.0, 0.0, -1.0, 2.0], 
                     [0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 3.0], 
                     [-1.0, 0.0, 1.0, 0.0, 1.0, -1.0, 0.0, 1.0]]
    output_basic_vars = [0, 4, 2, 3]

    assert all_stack_start.solve_linear_programming(basic_vars, matrix, n_decision_vars, is_max, n_artificials) == (output_basic_vars, output_matrix)

def test_solver23():

    matrix = [[-6,  4,  0,  0, -M, -M, 0],
              [ 3,  1,  1,  0,  0,  0, 5],
              [-6,  4,  0, -1,  1,  0, 2],
              [ 2,  5,  0,  0,  0,  1, 6]]
    basic_vars = [0, 3, 5, 6]
    n_decision_vars = 2
    n_artificials = 2
    is_max = False

    output_matrix = [[-7.6, 0.0, 0.0, 0.0, -1000000.0, -1000000.8, -4.8], 
                     [2.6, 0.0, 1.0, 0.0, 0.0, -0.2, 3.8], 
                     [0.4, 1.0, 0.0, 0.0, 0.0, 0.2, 1.2], 
                     [7.6, 0.0, 0.0, 1.0, -1.0, 0.8, 2.8]]
    output_basic_vars = [0, 3, 2, 4]

    assert all_stack_start.solve_linear_programming(basic_vars, matrix, n_decision_vars, is_max, n_artificials) == (output_basic_vars, output_matrix)


def test_solver26():

    matrix = [[0, -1/3, 0, -1/6, 0, 13/3],
              [0,  5/3, 1, -1/6, 0, 13/3],
              [1,  2/3, 0, -1/6, 0, 10/3],
              [0,   -1, 0,    0, 1,    2]]
    basic_vars = [0, 3, 1, 5]
    n_decision_vars = 2
    n_artificials = 1
    is_max = False

    output_matrix = None
    output_basic_vars = None

    assert all_stack_start.solve_linear_programming(basic_vars, matrix, n_decision_vars, is_max, n_artificials) == (output_basic_vars, output_matrix)

test_solver17()