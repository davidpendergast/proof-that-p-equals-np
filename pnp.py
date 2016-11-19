from problem import ALL_PROBLEMS
from bf import BrainfuckRunner
import program
import sys
import random

"""
Behold! A procedure that can solve any problem in polynomial time, assuming P=NP! It achieves 
this by generating all possible programs, and running each one for increasingly many steps until
it finds one that solves the problem. If P=NP, such a program must exist, and will be found 
eventually by this program.

Warning: Even if P=NP, this could take a long time before a solution is found!
"""

"""Selecting which problem to try"""
all_problems = ALL_PROBLEMS
print "Select a problem:"
for i in range(0, len(all_problems)):
    print str(i+1) +".\t"+ALL_PROBLEMS[i].name
choice = input("selection: ")
PROBLEM = ALL_PROBLEMS[(choice-1) % len(ALL_PROBLEMS)]
print ""

"""Creating the program runner, and starting the loops."""
PROGRAM_RUNNER = BrainfuckRunner(tape_length=100, cell_bits=8)
N = 1
while True: 
    for P in xrange(1, N+1):
        prog = PROGRAM_RUNNER.convert_program(P)
        if prog == None:
            output = None
        else:
            output = PROGRAM_RUNNER.run_program(prog, steps=N, problem_input=PROBLEM.input())
        
        """print the results of every hundred or so attempts"""
        if prog is not None and random.randint(0, 100) == 0:
            if output == None:
                output_str = "runtime error"
            else:
                output_str = str(output) if len(output) < 7 else str(output[:10])+"..."
            prog_str = "".join(prog).ljust(20)
            print "\tP = %s\t==>\t%s\t==>\t%s" % (str(P).ljust(10), prog_str, output_str)
        
        if output is not None and PROBLEM.is_correct(output):
            # holy crap we did it
            print "\nSolution found for problem: %s!" % PROBLEM.name
            print "P:       %d" % P
            print "N:       %d" % N
            print "program: %s" % "".join(prog)
            print "input:   %s" % PROBLEM.input()
            print "output:  %s" % output
            sys.exit()   
    N *= 2
