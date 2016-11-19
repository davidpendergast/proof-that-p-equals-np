ALL_PROBLEMS = []

def add_to_list(prob):
    ALL_PROBLEMS.append(prob)
    return prob

class Problem:
    def __init__(self, name, problem_input, verifier):
        """
        Args:
            name (string): Name of problem.
            input (:obj:`list` of int): Inputs that will be fed to Programs.
            verifier (:lambda: `list` of int -> boolean): Polynomial-time function that checks 
                the validity of a program output.
        """
        self.name = name
        self._input = problem_input
        self._verifier = verifier
        
    def is_correct(self, program_output):
        return self._verifier(program_output)
        
    def input(self):
        return self._input[:]
    

"""
Seeks a program that outputs at least one 7.
bf solution: +[+.]
"""
SEVEN_PROBLEM = add_to_list(Problem("Output a 7",[], lambda x : 7 in x))

"""
Seeks a program that outputs a single 3. 
bf solution: +++.
"""
SINGLE_THREE_PROBLEM = add_to_list(Problem("Output a Single 3", [], lambda x: x == [3]))

"""
Seeks a program that outputs the given inputs. 
bf solution: ,[.,]
"""
_oti_input = [36, 60, 24, 5]
OUTPUT_THE_INPUTS = add_to_list(Problem("Identity Function", _oti_input, lambda x: x == _oti_input))

"""
Swap two inputs.
bf solution: ,>,.<.
P = 251855
"""
SWAP_TWO_INPUTS = add_to_list(Problem("Swap Two Inputs", [32, -4], lambda x: len(x) == 2 and x[0] == -4 and x[1] == 32))


"""
Find the sum of two inputs.
bf solution: ,>,[<+>-]<.
P = big
"""
_v1 = 25
_v2 = 11
SUM_TWO_INPUTS = add_to_list(Problem("Sum Two Inputs", [_v1, _v2], lambda x: len(x) == 1 and x[0] == _v1 + _v2))

"""
Classic NP-Complete zero sum subset problem. 
bf poly-time solution: ????
"""
_zss_input_1 = [3, -3]
_zss_input_2 = [3, -2, -1]
_zss_input_3 = [1, 3, -5, 2, -4]
_input = _zss_input_1

def _check_zss(problem_input, output):
    return all(i in problem_input for i in output) and sum(output) == 0 and len(set(output)) == len(problem_input)
    
ZERO_SUM_SUBSET_1 = add_to_list(Problem("Zero Sum Subset 1", _zss_input_1, lambda x: _check_zss(_zss_input_1, x)))
ZERO_SUM_SUBSET_2 = add_to_list(Problem("Zero Sum Subset 2", _zss_input_2, lambda x: _check_zss(_zss_input_2, x)))
ZERO_SUM_SUBSET_3 = add_to_list(Problem("Zero Sum Subset 3", _zss_input_3, lambda x: _check_zss(_zss_input_3, x)))

        
