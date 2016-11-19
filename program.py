
class ProgramRunner:    
    def run_program(self, prog, steps, problem_input):
        """ Runs the given program on an input for a given number of steps and returns the output.
        Args:
            prog (boolean array): binary encoding of the program.
            steps (int): Upper bound on the number of instructions to execute in the program.
            input (list of ints): Input to be given to the program.
        
        Return:
            output (list of ints): A list of ints returned by the program, or an empty list if 
                nothing is returned. If the program fails due to a syntax or runtime error, None
                is returned.
        """
        return []
    
    def convert_program(self, prog_encoding):
        """ Attempts to convert the given program encoding into a format that run_program can run.
            This method may also attempt to remove simple errors to make the program more likely
            to run successfully. However there is no guarantee that the program will be valid upon 
            return from this method
        Args:
            prog_encoding (boolean array): The binary encoding of a program.
        """
        return prog
        

